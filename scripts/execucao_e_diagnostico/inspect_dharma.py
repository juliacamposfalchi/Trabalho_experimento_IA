import sys
from datasets import load_dataset

out = open(sys.argv[1], "w", encoding="utf-8")
ds = load_dataset("dharma-ai/DharmaOCR-Benchmark", split="test", streaming=True)
for i, row in enumerate(ds):
    if i >= 40:
        break
    img = row["image"]
    txt = row["assistant_without_json"]
    out.write(f"id={row['id']} size={img.size} chars={len(txt)} lines={txt.count(chr(10))+1}\n")
    out.write(repr(txt[:160]) + "\n\n")
out.close()
