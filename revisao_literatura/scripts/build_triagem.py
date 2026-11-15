import re, html, sys, unicodedata
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import CellIsRule

DL = Path(r"C:\Users\julia.falchi\Downloads")
ARQ = [("BibTeX(1)", DL / "Periodicos-CAPES-BibTex(1).bib"),
       ("BibTeX(2)", DL / "Periodicos-CAPES-BibTex(2).bib"),
       ("BibTeX (sem sufixo)", DL / "Periodicos-CAPES-BibTex.bib")]
OUT = Path(sys.argv[1])

def parse(path):
    recs, cur = [], None
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"@\S+\{(\w+),", line)
        if m:
            cur = {"id": m.group(1)}; recs.append(cur); continue
        m = re.match(r"(\w+)=\{(.*)\},?\s*$", line)
        if m and cur is not None:
            cur[m.group(1)] = html.unescape(html.unescape(m.group(2))).strip()
    return recs

def norm(t):
    t = unicodedata.normalize("NFKD", t.lower())
    return re.sub(r"[^a-z0-9]+", " ", "".join(c for c in t if not unicodedata.combining(c))).strip()

# Sugestões preliminares POR TÍTULO (a decisão final é da Julia)
LER = "Ler texto completo"
CONTEXTO = "Contexto (fundamentação)"
EXC = "Excluir"
S = {}
for i, mot in {
    "W3120871485": "Troca componentes de OCR em pipeline; pode ser comparação",
    "W4402012511": "Compara pré-processamentos com Tesseract",
    "W4403740341": "Efeito de pré-processamento no OCR (Tesseract)",
    "W2203103318": "Prevê acurácia de OCR a partir da binarização",
    "W2982358276": "Treinamento de motores de OCR",
    "W4286544596": "Pipeline de faturas; verificar se compara OCRs",
    "W4389762644": "Layout e detecção de linhas; verificar avaliação",
}.items(): S[i] = (LER, "", mot)
for i, mot in {
    "W2742651024": "Revisão de detecção de texto (fundamentação)",
    "W4392560291": "Dataset de ground truth de OCR (alemão histórico)",
    "W3081407480": "OCR neural com pós-correção (fundamentação)",
}.items(): S[i] = (CONTEXTO, "", mot)
E = {
 "E1 Manuscrito (HTR)": ["W4378528383"],
 "E2 Propõe modelo sem comparação": ["W3197118814","W3131997754","W3023805750","W4224229079","W4281679764","W3027621902","W2545564526"],
 "E3 Aplicação de ferramenta única": ["W4396237139","W4206518796","W4394975979","W4303184718","W4321364784","W4312048613","W2187888666","W3010275040","W4294988576","W2525158635","W2287144523","W3031443669","W3197860412","W3015803803","W4295082284","W3040497592","W2294484010","W3108992338"],
 "E4 Pós-correção, legenda ou NER": ["W4379793938","W4226476296","W4381853731","W4403246551","W4403246668"],
 "E5 Fora do tema": ["W2065939324","W4398185594","W4290994971","W3088654767","W4386525785"],
 "E6 Duplicado": ["W4239347571","W4241396795"],
}
for cod, ids in E.items():
    for i in ids: S[i] = (EXC, cod, "")
DUP_DE = {"W4239347571": "W2203103318", "W4241396795": "W3040497592"}

regs, vistos, dup_id = {}, {}, []
for rotulo, p in ARQ:
    for r in parse(p):
        if r["id"] in regs:
            regs[r["id"]]["buscas"].append(rotulo); dup_id.append((r["id"], rotulo)); continue
        r["buscas"] = [rotulo]; regs[r["id"]] = r

linhas = [r for r in regs.values() if r["id"] not in DUP_DE]
n_identificados = sum(1 for _ in ARQ for _ in parse(_[1]))
wb = Workbook()
thin = Side(style="thin", color="BBBBBB"); borda = Border(left=thin, right=thin, top=thin, bottom=thin)
hdr_fill = PatternFill("solid", fgColor="1F4E78"); hdr_font = Font(bold=True, color="FFFFFF")

def cabecalho(ws, cols, larguras):
    ws.append(cols)
    for c in ws[1]:
        c.fill, c.font, c.border = hdr_fill, hdr_font, borda
        c.alignment = Alignment(wrap_text=True, vertical="center")
    for i, w in enumerate(larguras, 1):
        ws.column_dimensions[ws.cell(1, i).column_letter].width = w
    ws.freeze_panes = "D2"

ws = wb.active; ws.title = "Triagem"
cabecalho(ws, ["Nº", "ID (CAPES/OpenAlex)", "Exportação(ões)", "Título", "Autores", "Ano", "Periódico", "DOI",
               "Sugestão preliminar (por título)", "Código sugerido", "Motivo da sugestão",
               "Decisão (título/resumo)", "Decisão (texto completo)", "Motivo final (E1 a E6)", "Observações"],
          [5, 14, 18, 60, 35, 7, 32, 28, 22, 26, 38, 18, 18, 22, 30])
sug_fill = {LER: "C6EFCE", CONTEXTO: "FFEB9C", EXC: "F8CBAD"}
for n, r in enumerate(linhas, 1):
    sug, cod, mot = S.get(r["id"], (EXC, "E5 Fora do tema", "Área não relacionada (casou com o termo OCR por outro motivo)"))
    ws.append([n, r["id"], ", ".join(r["buscas"]), r.get("title", ""), r.get("author", ""),
               int(r["year"]) if r.get("year", "").isdigit() else r.get("year", ""),
               r.get("journal", ""), r.get("doi", ""), sug, cod, mot, "", "", "", ""])
    ws.cell(n + 1, 9).fill = PatternFill("solid", fgColor=sug_fill.get(sug, "FFFFFF"))
for row in ws.iter_rows(min_row=2):
    for c in row:
        c.alignment = Alignment(wrap_text=True, vertical="top"); c.border = borda
last = ws.max_row
dv1 = DataValidation(type="list", formula1='"Incluir,Excluir,Dúvida"', allow_blank=True)
dv2 = DataValidation(type="list", formula1='"Incluir,Excluir"', allow_blank=True)
dv3 = DataValidation(type="list", formula1='"E1 Manuscrito (HTR),E2 Propõe modelo sem comparação,E3 Aplicação de ferramenta única,E4 Pós-correção/legenda/NER,E5 Fora do tema,E6 Duplicado,E7 Sem texto completo"', allow_blank=True)
for dv, col in ((dv1, "L"), (dv2, "M"), (dv3, "N")):
    ws.add_data_validation(dv); dv.add(f"{col}2:{col}{last}")
ws.auto_filter.ref = f"A1:O{last}"

# Duplicados removidos
wd = wb.create_sheet("Duplicados removidos")
cabecalho(wd, ["ID", "Título", "Tipo de duplicata", "Mantido como"], [14, 70, 34, 18])
for i, rot in dup_id:
    wd.append([i, regs[i].get("title", ""), f"Mesmo ID em {rot}", i])
for i, orig in DUP_DE.items():
    wd.append([i, regs[i].get("title", ""), "Mesmo título, outro ID", orig])
wd.freeze_panes = "A2"

# PRISMA
wp = wb.create_sheet("PRISMA")
wp.column_dimensions["A"].width = 58; wp.column_dimensions["B"].width = 14; wp.column_dimensions["C"].width = 60
wp.append(["Etapa", "Número", "Como é calculado"])
for c in wp[1]: c.fill, c.font = hdr_fill, hdr_font
wp.append(["Registros identificados (soma dos 3 arquivos)", n_identificados, "Valor fixo, dos exports do CAPES"])
wp.append(["Duplicados removidos", f"={n_identificados}-COUNTA(Triagem!B2:B{last})", "Identificados menos linhas da aba Triagem"])
wp.append(["Registros após remover duplicados", f"=COUNTA(Triagem!B2:B{last})", "Linhas da aba Triagem"])
wp.append(["Excluídos na triagem por título e resumo", f'=COUNTIF(Triagem!L2:L{last},"Excluir")', "Coluna L = Excluir"])
wp.append(["Textos completos avaliados", f'=COUNTIF(Triagem!L2:L{last},"Incluir")+COUNTIF(Triagem!L2:L{last},"Dúvida")', "Coluna L = Incluir ou Dúvida"])
wp.append(["Excluídos após leitura do texto completo", f'=COUNTIF(Triagem!M2:M{last},"Excluir")', "Coluna M = Excluir"])
wp.append(["Estudos incluídos na revisão", f'=COUNTIF(Triagem!M2:M{last},"Incluir")', "Coluna M = Incluir"])
wp.append([])
wp.append(["Sugestões preliminares (por título), para conferência", "", ""])
wp.cell(wp.max_row, 1).font = Font(bold=True)
for s in (LER, CONTEXTO, EXC, "Dúvida"):
    wp.append([s, f'=COUNTIF(Triagem!I2:I{last},"{s}")', ""])
wp.append([])
wp.append(["Atenção: as sugestões foram feitas só pelo título, sem ler resumo. As colunas L, M e N são de decisão sua.", "", ""])
wp.cell(wp.max_row, 1).alignment = Alignment(wrap_text=True)

# Critérios
wc = wb.create_sheet("Critérios")
wc.column_dimensions["A"].width = 12; wc.column_dimensions["B"].width = 90
for linha in [("Inclusão", "2018 a 2026; compara 2 ou mais ferramentas de OCR; métrica quantitativa (CER, WER, acurácia, tempo ou custo); imagens de documentos ou texto impresso; inglês ou português; texto completo acessível"),
              ("E1", "Manuscrito (HTR) como foco"), ("E2", "Propõe modelo novo sem comparar com outras ferramentas"),
              ("E3", "Aplicação de uma única ferramenta, sem comparação"), ("E4", "Pós-correção, legendagem de imagens, NER ou detecção sem avaliação de reconhecimento"),
              ("E5", "Fora do tema"), ("E6", "Duplicado"), ("E7", "Sem texto completo disponível")]:
    wc.append(linha)
for r in wc.iter_rows():
    r[0].font = Font(bold=True); r[1].alignment = Alignment(wrap_text=True, vertical="top")

wb.save(OUT)
print("identificados:", n_identificados, "| unicos:", len(linhas), "| dup_id:", len(dup_id), "| dup_titulo:", len(DUP_DE))
from collections import Counter
print(Counter(S.get(r["id"], (EXC,))[0] for r in linhas))
