import openpyxl, re, shutil
from openpyxl.styles import Font, PatternFill, Alignment

P = r"C:/Users/julia.falchi/Downloads/Mestrado Qualificação/triagem_prisma_ocr.xlsx"
shutil.copy(P, P.replace(".xlsx", "_backup_antes_decisoes.xlsx"))
wb = openpyxl.load_workbook(P)
ws = wb["Triagem"]
hdr = [c.value for c in ws[1]]
print(hdr)
col = {h: i + 1 for i, h in enumerate(hdr)}
cL = col["Decisão (título/resumo)"]; cM = col["Decisão (texto completo)"]; cN = col["Motivo final (E1 a E6)"]
cI = col["Sugestão preliminar (por título)"]; cJ = col["Código sugerido"]

# Decisões no texto completo (só resumos e metadados foram lidos; confirmar nos PDFs)
FT = {
    "Exchanging image processing": ("Incluir", "Compara Calamari e Tesseract 3 com CER (conferir texto completo)"),
    "ANALYSIS OF IMAGE PREPROCESSING": ("Excluir", "E3 Compara pré-processamentos, só Tesseract"),
    "Prediction of the Optical Character": ("Excluir", "E2 Propõe métrica de previsão, só Tesseract"),
    "COMPARISON OF THRESHOLDING": ("Excluir", "E3 Compara pré-processamentos, só Tesseract"),
    "Efficient and effective OCR engine": ("Excluir", "E2 Propõe fluxo de treinamento do Tesseract"),
    "Enhancing optical character": ("Excluir", "E2 Propõe métodos e dataset novo, sem comparar ferramentas"),
    "End to End Invoice": ("Excluir", "E4 Resumo não menciona OCR (detecção de tabelas); conferir texto completo"),
}
CONTEXTO = {  # marcados "Contexto" na sugestão: não elegíveis, ficam como apoio
    "Optical character recognition with neural networks and post-correction": "E4 Pós-correção (contexto)",
    "A review of algorithms for text detection": "E4 Detecção de texto, sem avaliação de reconhecimento (contexto)",
    "Reichsanzeiger-GT": "E5 Conjunto de dados de verdade de referência, não é comparação (contexto)",
}
fill = PatternFill("solid", fgColor="FFF2CC")
n_inc = n_exc = 0
for r in range(2, ws.max_row + 1):
    titulo = str(ws.cell(r, col["Título"]).value or "")
    sug = ws.cell(r, cI).value
    cod = str(ws.cell(r, cJ).value or "")
    if sug == "Excluir":
        ws.cell(r, cL, "Excluir"); ws.cell(r, cN, cod)
    elif sug == "Ler texto completo":
        ws.cell(r, cL, "Incluir")
        for k, (dec, mot) in FT.items():
            if titulo.startswith(k) or k.lower() in titulo.lower():
                ws.cell(r, cM, dec); ws.cell(r, cN, mot)
                break
        else:
            raise SystemExit("sem decisao: " + titulo)
    elif sug == "Contexto (fundamentação)":
        ws.cell(r, cL, "Excluir")
        for k, mot in CONTEXTO.items():
            if k.lower() in titulo.lower():
                ws.cell(r, cN, mot)
                break
        else:
            raise SystemExit("sem contexto: " + titulo)
    for c in (cL, cM, cN):
        ws.cell(r, c).fill = fill

# Aba de outras fontes (busca na web, não sistemática)
if "Outras fontes" in wb.sheetnames:
    del wb["Outras fontes"]
wo = wb.create_sheet("Outras fontes")
wo.append(["Nº", "Relato", "Origem", "Leitura realizada", "Decisão", "Motivo / observação"])
dados = [
    (1, "Kapelinski et al. (2026), Reading Brazil, ENIAC", "Busca na web", "PDF (corpo, conclusão e referências)", "Incluir", "Compara 14 motores, CER não, mas NED e FVR, em português, com tempo"),
    (2, "Nagayi et al. (2025), arXiv 2510.03570", "Busca na web / arXiv", "HTML completo", "Incluir", "Compara 4 ferramentas com CER, WER e tempo, em rótulos de embalagens"),
    (3, "Feng et al. (2026), arXiv 2602.02223", "Busca na web / arXiv", "Só o resumo", "Incluir", "Compara 4 ferramentas com acurácia por caractere. Confirmar no PDF"),
    (4, "Gómez Rey et al. (2026), arXiv 2608.24976", "Busca na web / arXiv", "Só o resumo", "Incluir", "Compara 13 abordagens com CER e WER, não só motores clássicos. Confirmar no PDF"),
    (5, "Puchol et al. (2026), arXiv 2605.29476", "Busca na web / arXiv", "Resumo", "Excluir", "E4 Compara tradução de imagens com texto, não OCR"),
]
for d in dados:
    wo.append(d)
for c in wo[1]:
    c.font = Font(bold=True)
for row in wo.iter_rows(min_row=2):
    for c in row:
        c.alignment = Alignment(wrap_text=True, vertical="top")
for l, w in zip("ABCDEF", [5, 48, 22, 32, 10, 70]):
    wo.column_dimensions[l].width = w

# Aba PRISMA: acrescenta o fluxo completo
wp = wb["PRISMA"]
r0 = wp.max_row + 2
linhas = [
    ("FLUXO PRISMA 2020 (bases + outras fontes)", None, None),
    ("Registros identificados nas bases (Periódicos CAPES, 3 buscas)", 76, "Valor fixo"),
    ("Removidos como duplicados", "=76-COUNTA(Triagem!B2:B70)", ""),
    ("Triados por título (resumo ausente nas exportações)", "=COUNTA(Triagem!B2:B70)", ""),
    ("Excluídos na triagem", '=COUNTIF(Triagem!L2:L70,"Excluir")', ""),
    ("Avaliados em detalhe (bases)", '=COUNTIF(Triagem!L2:L70,"Incluir")', "Só resumo e metadados lidos; texto completo não obtido"),
    ("Excluídos após avaliação (bases)", '=COUNTIF(Triagem!M2:M70,"Excluir")', ""),
    ("Incluídos vindos das bases", '=COUNTIF(Triagem!M2:M70,"Incluir")', ""),
    ("Relatos de outras fontes avaliados", "=COUNTA('Outras fontes'!A2:A6)", "Busca na web, não sistemática"),
    ("Excluídos de outras fontes", "=COUNTIF('Outras fontes'!E2:E6,\"Excluir\")", ""),
    ("Incluídos vindos de outras fontes", "=COUNTIF('Outras fontes'!E2:E6,\"Incluir\")", ""),
    ("TOTAL DE ESTUDOS INCLUÍDOS", f"=B{r0+7}+B{r0+10}", ""),
]
for i, (a, b, c) in enumerate(linhas):
    wp.cell(r0 + i, 1, a); wp.cell(r0 + i, 2, b); wp.cell(r0 + i, 3, c)
wp.cell(r0, 1).font = Font(bold=True)
wp.cell(r0 + 11, 1).font = Font(bold=True)
wp.cell(wp.max_row + 2, 1, "As colunas L, M e N da aba Triagem (amarelo) foram preenchidas por IA a partir de título, resumo e metadados. Confira cada uma, e leia os textos completos antes de relatar como 'avaliados'.")
wb.save(P)

# conferência
ws = wb["Triagem"]
from collections import Counter
print(Counter(ws.cell(r, cL).value for r in range(2, ws.max_row + 1)))
print(Counter(ws.cell(r, cM).value for r in range(2, ws.max_row + 1)))
