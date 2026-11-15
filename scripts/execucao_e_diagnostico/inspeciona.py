import openpyxl, io, sys
from pathlib import Path
scratchpad = Path("./scratchpad")
scratchpad.mkdir(exist_ok=True)
sys.stdout = io.open(scratchpad / "inspeciona.txt", "w", encoding="utf-8")
wb = openpyxl.load_workbook(r"C:/Users/julia.falchi/Downloads/Mestrado Qualificação/OCR - trabalho IA/triagem_prisma_ocr.xlsx")
for ws in wb:
    print("##", ws.title, ws.max_row, ws.max_column, "imagens:", len(ws._images))
ws = wb["Triagem"]
print([c.value for c in ws[1]])
for r in range(2, ws.max_row + 1):
    obs = ws.cell(r, 15).value
    if obs: print(r, "OBS:", obs)
import collections
print(collections.Counter(ws.cell(r, 12).value for r in range(2, ws.max_row+1)))
print(collections.Counter(ws.cell(r, 13).value for r in range(2, ws.max_row+1)))
