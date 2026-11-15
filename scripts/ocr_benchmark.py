# %% [markdown]
# # Benchmark de ferramentas de OCR (Tesseract, EasyOCR, PaddleOCR, docTR)
# Dataset: DharmaOCR-Benchmark (Hugging Face, dharma-ai/DharmaOCR-Benchmark), páginas em português.
# Passo 1 baixa uma amostra e grava em data/images, data/gt e data/manifest.csv.
# Passo 2 roda o experimento. Saída: resultados.csv (CER, WER e tempo por imagem, ferramenta e condição).
# Se quiser usar outro dataset, basta preencher data/images (imagens) e data/gt (um .txt por imagem)
# e pular o passo 1 (o manifest é opcional).

# %% Instalação (rodar só no Colab; no VS Code instale no ambiente virtual)
# !apt-get -qq install tesseract-ocr tesseract-ocr-por
# !pip -q install datasets pytesseract easyocr paddleocr paddlepaddle "python-doctr[torch]" surya-ocr jiwer scipy opencv-python-headless pandas matplotlib
# Para o cenário "só CPU" no Colab: Ambiente de execução > Alterar tipo > CPU (e o script já esconde a GPU).

# %% Configuração
import os
os.environ["CUDA_VISIBLE_DEVICES"] = ""   # cenário só com CPU: esconde a GPU de torch e paddle
from pathlib import Path
import re, time, unicodedata, json, platform, sys
import numpy as np, pandas as pd, cv2
import jiwer

DATA_DIR = Path("data")
IMG_DIR, GT_DIR = DATA_DIR / "images", DATA_DIR / "gt"
MANIFEST = DATA_DIR / "manifest.csv"
OUT_DIR = Path("resultados"); OUT_DIR.mkdir(exist_ok=True)
SEED = 42
rng = np.random.default_rng(SEED)

N_AMOSTRA = 60        # quantas páginas usar (aumente se o tempo permitir)
LADO_MAX = None       # redimensiona o maior lado para este valor (px); None mantém o original.
                      # TESTE PILOTO (8 páginas): reduzir para 2000 px destruiu as páginas grandes
                      # (2824 x 4268 px): o CER do Tesseract foi de 0,10 para 1,00 numa delas, porque o
                      # texto fica ilegível. Por isso o padrão agora é NÃO redimensionar. O custo é o
                      # tempo (páginas de até 3889 x 5792 px). Se redimensionar, declare no artigo.
# Ids a excluir depois de olhar as imagens (ex.: manuscritos do BRESSAY, que são outro tema, HTR)
EXCLUIR_IDS = {39, 43, 87, 110, 219, 305, 313, 345}   # manuscritos (BRESSAY) identificados por inspeção visual das imagens
MIN_CHARS_REF = 100   # descarta páginas quase vazias (ex.: id 214, referência de 8 caracteres), em que o CER é instável

# %% Passo 1: baixar e salvar a amostra (rodar uma vez)
# O dataset não traz uma coluna com o subconjunto (ESTER-Pt, Legal ou BRESSAY).
# Na inspeção das 40 primeiras linhas, a referência tem uma única linha (sem "\n") nas páginas
# sintéticas de texto corrido, e várias linhas nas páginas reais digitalizadas (livros antigos e
# documentos jurídicos). A coluna "tipo" abaixo usa essas regras como aproximação, e NÃO substitui
# a conferência visual das imagens.
# Palavras que sugerem documento jurídico ou administrativo (subconjunto "Legal", novo em relação
# ao Reading Brazil). É só uma suposição por palavras-chave: CONFIRME olhando as imagens e, se
# preciso, corrija a coluna "tipo" em data/manifest.csv antes de rodar o experimento.
# "Lei", "Art." etc. são sensíveis a maiúsculas de propósito: "lei" em minúscula aparece nos romances antigos.
PADRAO_JURIDICO = re.compile(
    r"(Art\.|§|\bLei\b|Decreto|(?i:tribut|jurídic|tribunal)|inciso|parágrafo único|DOUTRINA|CRÉDITO)")

def preparar_amostra():
    from datasets import load_dataset
    DATA_DIR.mkdir(exist_ok=True); IMG_DIR.mkdir(parents=True, exist_ok=True); GT_DIR.mkdir(parents=True, exist_ok=True)
    ds = load_dataset("dharma-ai/DharmaOCR-Benchmark", split="test")
    meta = ds.select_columns(["id", "assistant_without_json"])      # sem decodificar as imagens
    validos = {i for i, (pid, txt) in enumerate(zip(meta["id"], meta["assistant_without_json"]))
               if pid not in EXCLUIR_IDS and len(txt.strip()) >= MIN_CHARS_REF}
    # Ordem aleatória fixa sobre TODO o conjunto: excluir páginas só empurra as seguintes da fila,
    # sem trocar as que já foram inspecionadas.
    ordem = rng.permutation(len(ds))
    escolhidos = sorted(int(i) for i in [i for i in ordem if int(i) in validos][:N_AMOSTRA])
    linhas = []
    for i in escolhidos:
        row = ds[int(i)]
        img = row["image"].convert("RGB")
        w, h = img.size
        if LADO_MAX and max(w, h) > LADO_MAX:
            esc = LADO_MAX / max(w, h)
            img = img.resize((int(w * esc), int(h * esc)))
        nome = f"{row['id']:04d}"
        img.save(IMG_DIR / f"{nome}.png")
        txt = row["assistant_without_json"]
        (GT_DIR / f"{nome}.txt").write_text(txt, encoding="utf-8")
        if "\n" not in txt.strip():
            tipo = "sintetico_linha_unica"
        elif PADRAO_JURIDICO.search(txt):
            tipo = "real_juridico_provavel"
        else:
            tipo = "real_outro"
        linhas.append(dict(imagem=f"{nome}.png", id=row["id"], largura_orig=w, altura_orig=h,
                           caracteres_ref=len(txt), tipo=tipo))
    pd.DataFrame(linhas).to_csv(MANIFEST, index=False)
    print(pd.DataFrame(linhas)["tipo"].value_counts())

if not (IMG_DIR.exists() and any(IMG_DIR.glob("*.*"))):
    preparar_amostra()

# %% Normalização e métricas (mesma regra para todas as ferramentas)
def normalizar(texto: str) -> str:
    texto = unicodedata.normalize("NFC", texto)
    texto = re.sub(r"\s+", " ", texto)      # espaços e quebras de linha viram um espaço
    return texto.strip()

def metricas(ref: str, hip: str):
    ref, hip = normalizar(ref), normalizar(hip)
    if not ref:
        return np.nan, np.nan
    return jiwer.cer(ref, hip), jiwer.wer(ref, hip)

# %% Degradações controladas (a imagem original é a condição "original")
def ruido_gaussiano(img, sigma=25):
    ruido = rng.normal(0, sigma, img.shape).astype(np.float32)
    return np.clip(img.astype(np.float32) + ruido, 0, 255).astype(np.uint8)

def sal_pimenta(img, prop=0.05):
    # prop = fração de pixels afetados (metade pretos, metade brancos). Valor inicial a calibrar:
    # o Reading Brazil usa degradações do DocCreator, cujos parâmetros não estão no artigo.
    sorteio = rng.random(img.shape[:2])
    saida = img.copy()
    saida[sorteio < prop / 2] = 0
    saida[(sorteio >= prop / 2) & (sorteio < prop)] = 255
    return saida

def rotacionar(img, graus=5):
    h, w = img.shape[:2]
    M = cv2.getRotationMatrix2D((w / 2, h / 2), graus, 1.0)
    return cv2.warpAffine(img, M, (w, h), borderValue=(255, 255, 255))

def baixa_resolucao(img, fator=0.4):
    h, w = img.shape[:2]
    pequena = cv2.resize(img, (int(w * fator), int(h * fator)), interpolation=cv2.INTER_AREA)
    return cv2.resize(pequena, (w, h), interpolation=cv2.INTER_LINEAR)

CONDICOES = {
    "original": lambda im: im,
    "ruido_gaussiano": ruido_gaussiano,
    "sal_pimenta": sal_pimenta,
    "rotacao_5graus": rotacionar,
    "baixa_resolucao": baixa_resolucao,
}

# %% Ferramentas (cada uma recebe um array BGR e devolve texto)
import pytesseract
def run_tesseract(img):
    return pytesseract.image_to_string(img, lang="por")

import easyocr
_easy = easyocr.Reader(["pt"], gpu=False)
def run_easyocr(img):
    return " ".join(_easy.readtext(img, detail=0, paragraph=False))

from paddleocr import PaddleOCR
# confira a versão: a API 3.x usa .predict, a 2.x usa .ocr.
# enable_mkldnn=False evita um erro do oneDNN do Paddle 3.x em CPU (NotImplementedError em ConvertPirAttribute...);
# o restante fica no padrão do fabricante. Declare isso no método.
_paddle = PaddleOCR(lang="pt", enable_mkldnn=False)
def run_paddle(img):
    if hasattr(_paddle, "predict"):
        res = _paddle.predict(img)
        return " ".join(" ".join(r["rec_texts"]) for r in res)
    res = _paddle.ocr(img)
    return " ".join(l[1][0] for page in res if page for l in page)

from doctr.models import ocr_predictor
_doctr = ocr_predictor(pretrained=True)  # vocabulário limitado: acentos podem ser perdidos
def run_doctr(img):
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    doc = _doctr([rgb])
    return " ".join(w.value for p in doc.pages for b in p.blocks for l in b.lines for w in l.words)

FERRAMENTAS = {
    "Tesseract": run_tesseract,
    "EasyOCR": run_easyocr,
    "PaddleOCR": run_paddle,
    "docTR": run_doctr,
}

# Surya (opcional): foi o melhor motor de OCR no Reading Brazil, mas rodou em GPU lá.
# Em CPU tende a ser lento. A API do pacote muda entre versões; se falhar, o script segue sem ele.
USE_SURYA = True
if USE_SURYA:
    try:
        from PIL import Image
        from surya.detection import DetectionPredictor
        from surya.recognition import RecognitionPredictor
        _det, _rec = DetectionPredictor(), RecognitionPredictor()
        def run_surya(img):
            pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            res = _rec([pil], det_predictor=_det)
            return " ".join(l.text for l in res[0].text_lines)
        FERRAMENTAS["Surya"] = run_surya
    except Exception as e:
        print("Surya não carregado (confira a API da versão instalada):", e)

# %% Aquecimento (a primeira chamada de cada modelo é mais lenta e distorceria o tempo)
amostra = cv2.imread(str(next(IMG_DIR.glob("*.*"))))
for f in FERRAMENTAS.values():
    f(amostra)

# %% Experimento
HIP_DIR = OUT_DIR / "hipoteses"; HIP_DIR.mkdir(exist_ok=True)
T0 = time.time()
linhas = []
# Retomada: se o processo caiu, as páginas já gravadas em resultados_parcial.csv são puladas.
PARCIAL = OUT_DIR / "resultados_parcial.csv"
feitos = set()
if PARCIAL.exists():
    _p = pd.read_csv(PARCIAL)
    linhas = _p.to_dict("records")
    feitos = set(_p["imagem"])
    print(f"Retomando: {len(feitos)} páginas já concluídas", flush=True)
for img_path in sorted(IMG_DIR.glob("*.*")):
    if img_path.name in feitos:
        continue
    gt_path = GT_DIR / f"{img_path.stem}.txt"
    if not gt_path.exists():
        continue
    ref = gt_path.read_text(encoding="utf-8")
    base = cv2.imread(str(img_path))
    for cond, degradar in CONDICOES.items():
        img = degradar(base)  # mesma imagem degradada para todas as ferramentas
        for nome, run in FERRAMENTAS.items():
            t0 = time.perf_counter()
            try:
                hip = run(img)
            except Exception as e:
                hip = ""
                print(f"Erro em {nome} / {img_path.name} / {cond}: {e}")
            dt = time.perf_counter() - t0
            (HIP_DIR / f"{nome}__{cond}__{img_path.stem}.txt").write_text(hip, encoding="utf-8")  # para auditar erros
            cer, wer = metricas(ref, hip)
            linhas.append(dict(imagem=img_path.name, condicao=cond, ferramenta=nome,
                               cer=cer, wer=wer, tempo_s=dt))
    # progresso e salvamento parcial (se o processo cair, nada se perde)
    print(f"[{len({l['imagem'] for l in linhas})}] {img_path.name} concluída | {(time.time() - T0) / 60:.1f} min", flush=True)
    pd.DataFrame(linhas).to_csv(OUT_DIR / "resultados_parcial.csv", index=False)

df = pd.DataFrame(linhas)
if MANIFEST.exists():
    df = df.merge(pd.read_csv(MANIFEST)[["imagem", "tipo"]], on="imagem", how="left")
df.to_csv(OUT_DIR / "resultados.csv", index=False)

# %% Registro do ambiente (versões e hardware), para a seção de método
from importlib.metadata import version, PackageNotFoundError
def _v(pkg):
    try: return version(pkg)
    except PackageNotFoundError: return None
amb = {"python": sys.version.split()[0], "so": platform.platform(), "cpu": platform.processor(),
       "nucleos_logicos": os.cpu_count(), "gpu_visivel": os.environ.get("CUDA_VISIBLE_DEVICES") != "",
       "seed": SEED, "n_amostra": N_AMOSTRA, "lado_max_px": LADO_MAX,
       "pacotes": {p: _v(p) for p in ["pytesseract", "easyocr", "paddleocr", "paddlepaddle",
                                       "python-doctr", "surya-ocr", "jiwer", "opencv-python-headless"]}}
try: amb["tesseract"] = str(pytesseract.get_tesseract_version())
except Exception: amb["tesseract"] = None
try:
    import torch
    amb["torch_threads"] = torch.get_num_threads()   # EasyOCR e docTR usam esses fios; afeta o tempo
except Exception: amb["torch_threads"] = None
(OUT_DIR / "ambiente.json").write_text(json.dumps(amb, indent=2, ensure_ascii=False), encoding="utf-8")
print(json.dumps(amb, indent=2, ensure_ascii=False))

# %% Resumo por ferramenta e condição
resumo = (df.groupby(["ferramenta", "condicao"])[["cer", "wer", "tempo_s"]]
            .agg(["mean", "std"]).round(3))
print(resumo)
resumo.to_csv(OUT_DIR / "resumo.csv")

# %% Resumo por tipo de página (só condição original)
if "tipo" in df.columns:
    por_tipo = (df[df.condicao == "original"].groupby(["tipo", "ferramenta"])[["cer", "wer", "tempo_s"]]
                  .agg(["mean", "std", "count"]).round(3))
    print(por_tipo)
    por_tipo.to_csv(OUT_DIR / "resumo_por_tipo.csv")

# %% Gráfico de CER médio
import matplotlib.pyplot as plt
pivo = df.pivot_table(index="condicao", columns="ferramenta", values="cer", aggfunc="mean")
pivo.plot(kind="bar", figsize=(8, 4))
plt.ylabel("CER médio"); plt.xlabel("Condição"); plt.tight_layout()
plt.savefig(OUT_DIR / "cer_por_condicao.png", dpi=200)

# %% Intervalos de confiança (bootstrap, 95%) e testes pareados contra a linha de base
from scipy.stats import wilcoxon
def ic_boot(x, n=10000):
    x = np.asarray(x, dtype=float); x = x[~np.isnan(x)]
    r = np.random.default_rng(SEED)
    medias = [r.choice(x, len(x)).mean() for _ in range(n)]
    return np.percentile(medias, [2.5, 97.5])

linhas_ic = []
for (f, c), g in df.groupby(["ferramenta", "condicao"]):
    for m in ("cer", "wer"):
        lo, hi = ic_boot(g[m])
        linhas_ic.append(dict(ferramenta=f, condicao=c, metrica=m, media=g[m].mean(), ic95_inf=lo, ic95_sup=hi, n=g[m].count()))
ic = pd.DataFrame(linhas_ic).round(4)
ic.to_csv(OUT_DIR / "ic_bootstrap.csv", index=False)

BASE = "Tesseract"   # linha de base; os testes são pareados por imagem
testes = []
for c in df.condicao.unique():
    cer = df[df.condicao == c].pivot(index="imagem", columns="ferramenta", values="cer")
    outras = [f for f in cer.columns if f != BASE]
    for f in outras:
        par = cer[[BASE, f]].dropna()
        if len(par) >= 5 and (par[BASE] != par[f]).any():
            p = wilcoxon(par[BASE], par[f]).pvalue
            testes.append(dict(condicao=c, comparacao=f"{BASE} vs {f}", n=len(par),
                               diff_media_cer=(par[f] - par[BASE]).mean(), p_bruto=p,
                               p_bonferroni=min(1.0, p * len(outras) * df.condicao.nunique())))
pd.DataFrame(testes).round(4).to_csv(OUT_DIR / "testes_pareados.csv", index=False)
print(pd.DataFrame(testes).round(4))

# %% Testes das hipóteses H1 e H2 (Wilcoxon pareado por imagem, unilateral)
# H1: sem degradação, Tesseract e PaddleOCR têm CER/WER MENORES que o EasyOCR.
# H2: a rotação aumenta o CER/WER do Tesseract e do EasyOCR MAIS do que o do PaddleOCR
#     (perda = métrica na rotação menos métrica no original, por imagem).
# Correção de Bonferroni dentro de cada hipótese (2 comparações x 2 métricas = 4 testes).
COND_ORIG, COND_ROT = "original", "rotacao_5graus"

def teste_unilateral(a, b, alternativa):
    """a e b são séries indexadas por imagem. alternativa: 'less' testa a < b; 'greater' testa a > b."""
    par = pd.concat([a, b], axis=1, keys=["a", "b"]).dropna()
    if len(par) < 5 or (par["a"] == par["b"]).all():
        return dict(n=len(par), p_bruto=np.nan, media_dif=np.nan, mediana_dif=np.nan, ic95_inf=np.nan, ic95_sup=np.nan)
    d = par["a"] - par["b"]
    lo, hi = ic_boot(d)
    return dict(n=len(par), p_bruto=wilcoxon(par["a"], par["b"], alternative=alternativa).pvalue,
                media_dif=d.mean(), mediana_dif=d.median(), ic95_inf=lo, ic95_sup=hi)

def testar_h1_h2(base, grupo):
    resultados = []
    for m in ("cer", "wer"):
        P = base.pivot_table(index="imagem", columns=["condicao", "ferramenta"], values=m)
        ferr = set(P.columns.get_level_values("ferramenta"))
        if not {"Tesseract", "EasyOCR", "PaddleOCR"} <= ferr or COND_ORIG not in P.columns.get_level_values(0):
            continue
        for a in ("Tesseract", "PaddleOCR"):  # H1: a < EasyOCR
            r = teste_unilateral(P[(COND_ORIG, a)], P[(COND_ORIG, "EasyOCR")], "less")
            resultados.append(dict(grupo=grupo, hipotese="H1", metrica=m, comparacao=f"{a} < EasyOCR (original)", **r))
        if COND_ROT in P.columns.get_level_values(0):
            perda = {f: P[(COND_ROT, f)] - P[(COND_ORIG, f)] for f in ("Tesseract", "EasyOCR", "PaddleOCR")}
            for a in ("Tesseract", "EasyOCR"):  # H2: perda de a > perda do PaddleOCR
                r = teste_unilateral(perda[a], perda["PaddleOCR"], "greater")
                resultados.append(dict(grupo=grupo, hipotese="H2", metrica=m, comparacao=f"perda por rotação: {a} > PaddleOCR", **r))
    t = pd.DataFrame(resultados)
    if not t.empty:
        t["p_bonferroni"] = t.groupby(["grupo", "hipotese"])["p_bruto"].transform(lambda s: (s * s.notna().sum()).clip(upper=1.0))
    return t

tabelas = [testar_h1_h2(df, "todos")]
if "tipo" in df.columns:   # análise exploratória por tipo de página (sem hipótese própria)
    for tp, sub in df.groupby("tipo"):
        tabelas.append(testar_h1_h2(sub, f"exploratorio:{tp}"))
h1h2 = pd.concat([t for t in tabelas if not t.empty], ignore_index=True).round(4)
h1h2.to_csv(OUT_DIR / "testes_H1_H2.csv", index=False)
print(h1h2.to_string())
# Leitura: mediana_dif e media_dif negativas em H1 (a < EasyOCR) e positivas em H2 (perda maior)
# apoiam a hipótese; só considere confirmada com p_bonferroni < 0,05 e IC95 coerente com a direção.
