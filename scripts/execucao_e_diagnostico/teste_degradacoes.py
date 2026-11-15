import re, sys, numpy as np, cv2
src = open(sys.argv[1], encoding="utf-8").read()
ini = src.index("def ruido_gaussiano"); fim = src.index("CONDICOES = {")
ns = {"np": np, "cv2": cv2, "rng": np.random.default_rng(42)}
exec(src[ini:fim], ns)
img = np.full((400, 300, 3), 255, np.uint8)
cv2.putText(img, "Teste OCR", (20, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
for nome in ["ruido_gaussiano", "sal_pimenta", "rotacionar", "baixa_resolucao"]:
    out = ns[nome](img)
    print(nome, out.shape, out.dtype, "diferenca media:", round(float(np.abs(out.astype(int) - img.astype(int)).mean()), 2))
sp = ns["sal_pimenta"](img)
frac = ((sp == 0).all(axis=2) | (sp == 255).all(axis=2)).mean()
print("sal_pimenta: fracao de pixels extremos ~", round(float(frac), 3))
pad = re.compile(r"(Art\.|§|\bLei\b|Decreto|tribut|jurídic|Tribunal|inciso|parágrafo único|DOUTRINA|CRÉDITO)", re.I)
amostras = {"id7 DOUTRINA NACIONAL": "DOUTRINA NACIONAL\n179\n132/2023", "id28": "CRÉDITO\nTRIBUTÁRIO",
            "id36 Lei": "8 Lei 12.514/2011: \"Art. 3º", "id13 literatura": "5 HISTORIAS SEM DATAS \n\n\n—Olhai bem. Muitos corpos",
            "id26 literatura": "–25–\n\n mãi falta um élo. Creio que"}
for k, v in amostras.items(): print(k, "->", bool(pad.search(v)))
