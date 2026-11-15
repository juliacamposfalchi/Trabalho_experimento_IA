import openpyxl, collections
ws = openpyxl.load_workbook(r"C:/Users/julia.falchi/Downloads/Mestrado Qualificação/triagem_prisma_ocr.xlsx")["Triagem"]
c = collections.Counter()
for r in range(2, ws.max_row + 1):
    if ws.cell(r, 12).value == "Excluir":
        c[str(ws.cell(r, 14).value)[:2]] += 1
print(c, sum(c.values()))
