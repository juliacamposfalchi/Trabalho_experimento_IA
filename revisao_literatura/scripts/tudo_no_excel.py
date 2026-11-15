import openpyxl, re, io, json, shutil, glob, os
import pandas as pd
from pathlib import Path
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.drawing.image import Image as XLImage
from openpyxl.utils import get_column_letter

BASE = Path(r"C:/Users/julia.falchi/Downloads/Mestrado Qualificação")
PASTA = BASE / "OCR - trabalho IA"
R = PASTA / "resultados_40pag"
XLSX = PASTA / "triagem_prisma_ocr.xlsx"
SP = Path("./scratchpad")
SP.mkdir(exist_ok=True)
shutil.copy(XLSX, SP / "triagem_antes_de_tudo.xlsx")

ILEGAL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")
def limpa(v):
    if isinstance(v, str):
        v = ILEGAL.sub("", v)
        return v[:32000]
    return v

def le_csv(p):
    for enc in ("utf-8-sig", "cp1252"):
        try:
            return pd.read_csv(p, encoding=enc, header=0)
        except UnicodeDecodeError:
            continue
    raise SystemExit("encoding " + str(p))

wb = openpyxl.load_workbook(XLSX)
for n in ["Leia-me", "Resultados", "Resumo por condição", "Resumo por tipo", "IC bootstrap", "Testes H1 H2",
          "Testes sem caixa", "Manifesto", "Referências", "Saídas do OCR", "Ambiente", "Gráfico CER", "Diagrama PRISMA",
          "Artigo (rascunho)", "Protocolo", "Extração CAPES", "Extração web"]:
    if n in wb.sheetnames:
        del wb[n]

HDR = PatternFill("solid", fgColor="DCE9F7")
def df_para_aba(nome, df, larguras=None, num_fmt=None, wrap=False):
    ws = wb.create_sheet(nome)
    ws.append([str(c) for c in df.columns])
    for row in df.itertuples(index=False):
        ws.append([limpa(None if (isinstance(v, float) and pd.isna(v)) else v) for v in row])
    for c in ws[1]:
        c.font = Font(bold=True); c.fill = HDR
        c.alignment = Alignment(wrap_text=True, vertical="center")
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions
    for i, col in enumerate(df.columns, 1):
        w = (larguras or {}).get(col) or min(max(len(str(col)) + 2, 12), 28)
        ws.column_dimensions[get_column_letter(i)].width = w
    if num_fmt:
        for row in ws.iter_rows(min_row=2):
            for c in row:
                if isinstance(c.value, float):
                    c.number_format = num_fmt
    if wrap:
        for row in ws.iter_rows(min_row=2):
            for c in row:
                c.alignment = Alignment(wrap_text=True, vertical="top")
    return ws

# Resultados por página (com CER/WER sem caixa)
res = le_csv(R / "resultados_sem_caixa.csv")
res = res.rename(columns={"cer": "CER", "wer": "WER", "cer_ci": "CER sem caixa", "wer_ci": "WER sem caixa", "tempo_s": "tempo (s)"})
df_para_aba("Resultados", res, num_fmt="0.000")

# Resumos
def csv_cru(nome_aba, arq):
    ws = wb.create_sheet(nome_aba)
    for line in io.open(R / arq, encoding="utf-8-sig").read().splitlines():
        ws.append([limpa(float(x) if re.fullmatch(r"-?\d+\.\d+", x) else x) for x in line.split(",")])
    for c in ws[1]:
        c.font = Font(bold=True)
    for i in range(1, ws.max_column + 1):
        ws.column_dimensions[get_column_letter(i)].width = 16
    return ws
ws = csv_cru("Resumo por condição", "resumo.csv")
r0 = ws.max_row + 3
ws.cell(r0 - 1, 1, "Mesma tabela, com CER e WER sem distinção de maiúsculas (colunas cer_ci e wer_ci):").font = Font(bold=True)
for i, line in enumerate(io.open(R / "resumo_sem_caixa.csv", encoding="utf-8-sig").read().splitlines()):
    for j, x in enumerate(line.split(",")):
        ws.cell(r0 + i, j + 1, float(x) if re.fullmatch(r"-?\d+\.\d+", x) else x)
csv_cru("Resumo por tipo", "resumo_por_tipo.csv")
df_para_aba("IC bootstrap", le_csv(R / "ic_bootstrap.csv"), larguras={"comparacao": 50}, num_fmt="0.000")
df_para_aba("Testes H1 H2", le_csv(R / "testes_H1_H2.csv"), larguras={"comparacao": 52, "grupo": 38}, num_fmt="0.0000")
df_para_aba("Testes sem caixa", le_csv(R / "testes_sem_caixa.csv"), larguras={"comparacao": 52}, num_fmt="0.0000")
man = le_csv(R / "manifest.csv")
df_para_aba("Manifesto", man, larguras={"tipo": 26})

# Referências (transcrições de referência) e saídas do OCR
gt_dir = Path(r"//wsl.localhost/Ubuntu-24.04/home/juliafalchi/ocrtest/work/data/gt")
refs = []
for img in man["imagem"]:
    stem = img.replace(".png", "")
    f = gt_dir / f"{stem}.txt"
    refs.append(f.read_text(encoding="utf-8") if f.exists() else "(não encontrada)")
dfr = man[["imagem", "tipo", "caracteres_ref"]].copy(); dfr["referência (transcrição)"] = refs
ws = df_para_aba("Referências", dfr, larguras={"referência (transcrição)": 120, "tipo": 26}, wrap=True)

linhas = []
for f in sorted((R / "hipoteses").glob("*.txt")):
    ferr, cond, stem = f.stem.split("__")
    linhas.append((ferr, cond, stem + ".png", f.read_text(encoding="utf-8", errors="replace")))
dfo = pd.DataFrame(linhas, columns=["ferramenta", "condição", "imagem", "texto reconhecido"])
df_para_aba("Saídas do OCR", dfo, larguras={"texto reconhecido": 120, "condição": 18}, wrap=False)

# Ambiente
amb = json.loads((R / "ambiente.json").read_text(encoding="utf-8"))
ws = wb.create_sheet("Ambiente")
ws.append(["item", "valor"]); ws["A1"].font = Font(bold=True); ws["B1"].font = Font(bold=True)
for k, v in amb.items():
    if isinstance(v, dict):
        for k2, v2 in v.items():
            ws.append([f"{k}.{k2}", str(v2)])
    else:
        ws.append([k, str(v)])
ws.column_dimensions["A"].width = 30; ws.column_dimensions["B"].width = 60

# Imagens
for nome, arq in [("Gráfico CER", R / "cer_por_condicao.png"), ("Diagrama PRISMA", PASTA / "prisma_fluxo.png")]:
    ws = wb.create_sheet(nome)
    img = XLImage(str(arq))
    esc = 1000 / img.width if img.width > 1000 else 1
    img.width, img.height = img.width * esc, img.height * esc
    ws.add_image(img, "A1")

# Textos em linhas
def texto_para_aba(nome, arq):
    ws = wb.create_sheet(nome)
    ws.column_dimensions["A"].width = 160
    for line in io.open(arq, encoding="utf-8-sig", errors="replace").read().splitlines():
        ws.append([limpa(line)])
        ws.cell(ws.max_row, 1).alignment = Alignment(wrap_text=True, vertical="top")
    return ws
texto_para_aba("Artigo (rascunho)", PASTA / "artigo_ocr_rascunho.txt")
texto_para_aba("Protocolo", BASE / "protocolo_revisao_sistematica.md")
texto_para_aba("Extração CAPES", BASE / "extracao_7_artigos.md")
texto_para_aba("Extração web", BASE / "extracao_estudos_web.md")

# Leia-me
ws = wb.create_sheet("Leia-me", 0)
linhas = [
    ("ESTUDO DE OCR: tudo em um só arquivo", ""),
    ("", ""),
    ("Aba", "O que contém"),
    ("Triagem, Duplicados removidos, PRISMA, Critérios, Outras fontes", "Revisão da literatura (colunas L, M e N da Triagem foram preenchidas por IA, só com título, resumo e metadados: conferir)"),
    ("Diagrama PRISMA", "Fluxograma PRISMA 2020 (imagem)"),
    ("Resultados", "800 linhas (40 páginas x 4 ferramentas x 5 condições): CER, WER, CER e WER sem distinção de maiúsculas, tempo e tipo da página"),
    ("Resumo por condição", "Médias por ferramenta e condição (primeira tabela com caixa, segunda sem caixa)"),
    ("Resumo por tipo", "Médias na condição original por tipo de documento (com distinção de caixa)"),
    ("IC bootstrap", "Intervalos de confiança de 95% (10.000 reamostragens, semente 42)"),
    ("Testes H1 H2", "Testes de Wilcoxon pareados unilaterais, métricas com distinção de caixa (grupo 'todos' = análise principal; 'exploratorio:...' = por tipo, sem correção entre grupos)"),
    ("Testes sem caixa", "Os mesmos testes com CER e WER sem distinção de maiúsculas (análise adicional)"),
    ("Manifesto", "Tamanho em pixels, caracteres da referência e tipo de cada página. O tipo 'sintetico_linha_unica' significa só 'referência sem quebra de linha' e não foi conferido visualmente"),
    ("Referências", "Transcrição de referência de cada uma das 40 páginas"),
    ("Saídas do OCR", "O texto que cada ferramenta leu, em cada condição (800 linhas), para comparar com a referência"),
    ("Gráfico CER", "CER médio por condição"),
    ("Ambiente", "Versões das ferramentas e do computador"),
    ("Artigo (rascunho)", "Texto atual do artigo, uma linha por parágrafo"),
    ("Protocolo, Extração CAPES, Extração web", "Protocolo da revisão e fichas de extração dos estudos"),
    ("", ""),
    ("Não está aqui", "As imagens das 40 páginas (ficam em \\\\wsl.localhost\\Ubuntu-24.04\\home\\juliafalchi\\ocrtest\\work\\data\\images) e os scripts ocr_benchmark.py e reanalise_caixa.py"),
]
for l in linhas:
    ws.append(list(l))
ws["A1"].font = Font(bold=True, size=14)
for c in ws[3]:
    c.font = Font(bold=True); c.fill = HDR
ws.column_dimensions["A"].width = 58; ws.column_dimensions["B"].width = 140
for row in ws.iter_rows(min_row=3):
    for c in row:
        c.alignment = Alignment(wrap_text=True, vertical="top")

wb.save(XLSX)
print("salvo", XLSX.stat().st_size, wb.sheetnames)
