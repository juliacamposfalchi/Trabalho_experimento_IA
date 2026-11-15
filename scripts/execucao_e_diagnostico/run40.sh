#!/bin/bash
export PYTHONNOUSERSITE=1
export PYTHONIOENCODING=utf-8
export HF_HUB_DISABLE_SYMLINKS_WARNING=1
export TESSDATA_PREFIX=$HOME/ocrtest/tessdata
export PATH=$HOME/ocrtest/mm/bin:$PATH
export PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK=True
cd ~/ocrtest
[ -d work ] && rm -rf work_piloto_8pag && mv work work_piloto_8pag
mkdir -p work && cd work
SRC="$HOME/ocrtest/scratchpad/ocr_benchmark_src.py"
cp "$SRC" ocr_benchmark.py
sed -i 's/^N_AMOSTRA = 60.*/N_AMOSTRA = 40/' ocr_benchmark.py
grep -nE "^N_AMOSTRA|^LADO_MAX" ocr_benchmark.py
echo "== inicio: $(date) =="
~/ocrtest/py/bin/python ocr_benchmark.py
echo "== fim: $(date) =="
echo "== RUN40_DONE =="
