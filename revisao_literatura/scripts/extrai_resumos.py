import re, io, glob
from pathlib import Path
out = io.open(Path("./scratchpad") / "abstracts.txt", "w", encoding="utf-8")
seen = set()
for f in sorted(glob.glob(r"C:/Users/julia.falchi/Downloads/Periodicos-CAPES-BibTex*.bib")):
    t = io.open(f, encoding="utf-8").read()
    for e in re.split(r"\n@", t):
        ti = re.search(r"title\s*=\s*\{(.+?)\},?\s*\n", e, re.S)
        ab = re.search(r"abstract\s*=\s*\{(.+?)\},?\s*\n", e, re.S)
        if not ti:
            continue
        k = ti.group(1).strip()[:80]
        if k in seen:
            continue
        seen.add(k)
        out.write("## " + ti.group(1).strip()[:150] + "\n" + (re.sub(r"\s+", " ", ab.group(1))[:800] if ab else "(sem resumo)") + "\n\n")
out.close()
print(len(seen))
