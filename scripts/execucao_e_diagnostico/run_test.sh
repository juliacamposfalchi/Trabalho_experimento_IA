#!/bin/bash
set -e
export PYTHONNOUSERSITE=1
export PYTHONIOENCODING=utf-8
export HF_HUB_DISABLE_SYMLINKS_WARNING=1
export TESSDATA_PREFIX=$HOME/ocrtest/tessdata
export PATH=$HOME/ocrtest/mm/bin:$PATH
export PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK=True
rm -rf ~/ocrtest/work && mkdir -p ~/ocrtest/work && cd ~/ocrtest/work
SRC="$HOME/ocrtest/scratchpad/ocr_benchmark_src.py"
cp "$SRC" ocr_benchmark.py
sed -i 's/^N_AMOSTRA = 60.*/N_AMOSTRA = 8/' ocr_benchmark.py
grep -n "^N_AMOSTRA" ocr_benchmark.py
echo "== rodando =="
time ~/ocrtest/py/bin/python ocr_benchmark.py
echo "== RUN_DONE =="
ls -la resultados data | head -40
