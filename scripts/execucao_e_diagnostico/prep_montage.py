import sys, os, re
os.environ["CUDA_VISIBLE_DEVICES"] = ""
src = open(sys.argv[1], encoding="utf-8").read()
fim = src.index("# %% Normalização e métricas")
exec(src[:fim])                      # configuração + preparar_amostra (grava data/images, data/gt, manifest)
import numpy as np, cv2, pandas as pd
man = pd.read_csv(MANIFEST)
print(man.tipo.value_counts().to_string())
print(man[["id", "largura_orig", "altura_orig", "caracteres_ref", "tipo"]].to_string(index=False))
out = sys.argv[2]
tw, th, cols = 250, 330, 5
for parte, bloco in enumerate([man.iloc[k:k + 20] for k in range(0, len(man), 20)]):
    linhas = []
    for k in range(0, len(bloco), cols):
        cel = []
        for _, r in bloco.iloc[k:k + cols].iterrows():
            im = cv2.imread(str(IMG_DIR / r.imagem))
            h, w = im.shape[:2]; esc = min(tw / w, (th - 20) / h)
            im = cv2.resize(im, (max(1, int(w * esc)), max(1, int(h * esc))), interpolation=cv2.INTER_AREA)
            tela = np.full((th, tw, 3), 255, np.uint8)
            tela[20:20 + im.shape[0], :im.shape[1]] = im
            cv2.putText(tela, f"id {r.id} {r.tipo[:12]}", (2, 14), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 200), 1)
            cel.append(tela)
        while len(cel) < cols: cel.append(np.full((th, tw, 3), 255, np.uint8))
        linhas.append(np.hstack(cel))
    cv2.imwrite(f"{out}_{parte + 1}.png", np.vstack(linhas))
print("montagens ok")
