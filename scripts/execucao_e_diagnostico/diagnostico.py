import re, unicodedata, time
import numpy as np, cv2, jiwer, pytesseract
from datasets import load_dataset

def norm(t):
    return re.sub(r"\s+", " ", unicodedata.normalize("NFC", t)).strip()

ds = load_dataset("dharma-ai/DharmaOCR-Benchmark", split="test")
alvo = {42: "sintetico", 213: "sintetico grande", 424: "sintetico grande", 43: "real_outro", 321: "juridico", 379: "juridico"}
idx = {ds[i]["id"]: i for i in range(len(ds))}
print(f"{'id':>4} {'tipo':<18} {'orig(px)':<12} {'CER orig':>9} {'CER 2000px':>11} {'len ref':>8} {'len hip orig':>13} {'len hip 2000':>13}")
for i, tipo in alvo.items():
    row = ds[idx[i]]
    im = cv2.cvtColor(np.array(row["image"].convert("RGB")), cv2.COLOR_RGB2BGR)
    ref = norm(row["assistant_without_json"])
    h, w = im.shape[:2]
    esc = 2000 / max(h, w)
    im2 = cv2.resize(im, (int(w * esc), int(h * esc))) if esc < 1 else im
    ho = norm(pytesseract.image_to_string(im, lang="por"))
    h2 = norm(pytesseract.image_to_string(im2, lang="por"))
    print(f"{i:>4} {tipo:<18} {str((w, h)):<12} {jiwer.cer(ref, ho):>9.3f} {jiwer.cer(ref, h2):>11.3f} {len(ref):>8} {len(ho):>13} {len(h2):>13}")
    if i == 42:
        print("  REF :", ref[:200]); print("  HIP :", ho[:200])
