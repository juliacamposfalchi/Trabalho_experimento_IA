# Reanálise secundária: CER/WER sem distinção de maiúsculas e minúsculas.
# Análise ADICIONAL, decidida depois de ver os dados (páginas em caixa alta com referência em caixa mista).
# A métrica principal continua sendo a original (com distinção de caixa).
# Uso: dentro da pasta do experimento (que contém data/ e resultados/): python reanalise_caixa.py
import re, unicodedata, itertools
from pathlib import Path
import numpy as np, pandas as pd, jiwer
from scipy.stats import wilcoxon

D, R = Path("data"), Path("resultados")
SEED, N_BOOT = 42, 10_000
rng = np.random.default_rng(SEED)

def norm(t):
    t = unicodedata.normalize("NFC", t).casefold()
    return re.sub(r"\s+", " ", t).strip()

res = pd.read_csv(R / "resultados.csv")
res["stem"] = res["imagem"].str.replace(".png", "", regex=False)

cer_ci, wer_ci = [], []
for _, r in res.iterrows():
    ref = norm((D / "gt" / f"{r.stem}.txt").read_text(encoding="utf-8"))
    f = R / "hipoteses" / f"{r.ferramenta}__{r.condicao}__{r.stem}.txt"
    hip = norm(f.read_text(encoding="utf-8")) if f.exists() else ""
    cer_ci.append(jiwer.cer(ref, hip)); wer_ci.append(jiwer.wer(ref, hip))
res["cer_ci"], res["wer_ci"] = cer_ci, wer_ci
res.drop(columns="stem").to_csv(R / "resultados_sem_caixa.csv", index=False)

# resumo
resumo = res.groupby(["ferramenta", "condicao"])[["cer", "cer_ci", "wer", "wer_ci"]].mean().round(3)
resumo.to_csv(R / "resumo_sem_caixa.csv")
print(resumo.to_string())

def boot_ic(x):
    x = np.asarray(x); m = [rng.choice(x, len(x)).mean() for _ in range(N_BOOT)]
    return np.percentile(m, [2.5, 97.5])

linhas = []
for met in ["cer", "cer_ci", "wer", "wer_ci"]:
    p = res.pivot_table(index="imagem", columns=["ferramenta", "condicao"], values=met)
    for t in ["Tesseract", "PaddleOCR", "EasyOCR", "docTR"]:
        lo, hi = boot_ic(p[(t, "original")])
        linhas.append(dict(tipo="IC_original", metrica=met, comparacao=t, media=p[(t, "original")].mean(), ic_inf=lo, ic_sup=hi))
    def teste(a, b, nome, hip):
        d = a - b
        pv = wilcoxon(d, alternative="less" if hip == "H1" else "greater").pvalue if (d != 0).any() else 1.0
        lo, hi = boot_ic(d)
        return dict(tipo=hip, metrica=met, comparacao=nome, n=len(d), p_bruto=pv, p_bonf=min(1, pv * 2),
                    media_dif=d.mean(), mediana_dif=np.median(d), ic_inf=lo, ic_sup=hi)
    for t in ["Tesseract", "PaddleOCR"]:
        linhas.append(teste(p[(t, "original")], p[("EasyOCR", "original")], f"{t} < EasyOCR (original)", "H1"))
    perda = lambda t: p[(t, "rotacao_5graus")] - p[(t, "original")]
    for t in ["Tesseract", "EasyOCR"]:
        linhas.append(teste(perda(t), perda("PaddleOCR"), f"perda por rotacao: {t} > PaddleOCR", "H2"))
out = pd.DataFrame(linhas).round(4)
out.to_csv(R / "testes_sem_caixa.csv", index=False)
print(out.to_string())

# checagem de tempo: as 11 últimas páginas rodaram depois do reinício do WSL
man = pd.read_csv(D / "manifest.csv")
man["mpx"] = man.largura_orig * man.altura_orig / 1e6
ordem = sorted(man["imagem"]); ult = set(ordem[29:])
t = res[res.condicao == "original"].merge(man[["imagem", "mpx"]], on="imagem")
t["sessao"] = np.where(t.imagem.isin(ult), "retomada(11)", "inicial(29)")
t["s_por_mpx"] = t.tempo_s / t.mpx
print(t.groupby(["ferramenta", "sessao"])["s_por_mpx"].median().round(2).unstack().to_string())
