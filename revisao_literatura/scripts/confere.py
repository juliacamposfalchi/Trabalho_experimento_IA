import openpyxl, io, sys
from pathlib import Path
scratchpad = Path("./scratchpad")
scratchpad.mkdir(exist_ok=True)
sys.stdout = io.open(scratchpad / "confere.txt", "w", encoding="utf-8")
wb = openpyxl.load_workbook(r"C:/Users/julia.falchi/Downloads/Mestrado Qualificação/OCR - trabalho IA/triagem_prisma_ocr.xlsx")
for ws in wb: print(ws.title, ws.max_row, ws.max_column, len(ws._images))
ws = wb["Resumo por condição"]
for r in ws.iter_rows(min_row=1, max_row=6, values_only=True): print(r)
ws = wb["Saídas do OCR"]; print([c.value for c in ws[1]]); print(str(ws.cell(2,4).value)[:80])
ws = wb["Referências"]; print(str(ws.cell(2,4).value)[:80])
ws = wb["PRISMA"]
for r in ws.iter_rows(min_row=17, values_only=True): print(r)
