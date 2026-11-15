import sys, numpy as np, pandas as pd
from pathlib import Path
src = open(sys.argv[1], encoding="utf-8").read()
a = src.index("from scipy.stats import wilcoxon"); b = src.index("linhas_ic = []")
c = src.index("# %% Testes das hipóteses H1 e H2")
rng = np.random.default_rng(1)
linhas = []
for i in range(40):
    tipo = ["sintetico_linha_unica", "real_juridico_provavel", "real_outro"][i % 3]
    base = {"Tesseract": .08, "PaddleOCR": .07, "EasyOCR": .18, "docTR": .12}
    perda = {"Tesseract": .30, "EasyOCR": .30, "PaddleOCR": .05, "docTR": .25}
    for f in base:
        o = max(0, base[f] + rng.normal(0, .02))
        r = o + max(0, perda[f] + rng.normal(0, .05))
        for cond, v in (("original", o), ("rotacao_5graus", r)):
            linhas.append(dict(imagem=f"{i:04d}.png", condicao=cond, ferramenta=f, cer=v, wer=v * 1.5, tipo=tipo))
ns = {"np": np, "pd": pd, "SEED": 42, "OUT_DIR": Path(sys.argv[2]), "df": pd.DataFrame(linhas)}
ns["OUT_DIR"].mkdir(exist_ok=True)
exec(src[a:b] + src[c:], ns)
