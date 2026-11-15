import openpyxl
p = r"C:/Users/julia.falchi/Downloads/Mestrado Qualificação/OCR - trabalho IA/triagem_prisma_ocr.xlsx"
wb = openpyxl.load_workbook(p)
for n in list(wb.sheetnames):
    if n.endswith("condição1"):
        del wb[n]
wb.save(p)
print(wb.sheetnames)
