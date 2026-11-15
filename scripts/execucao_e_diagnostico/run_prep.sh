#!/bin/bash
export PYTHONNOUSERSITE=1 PYTHONIOENCODING=utf-8 HF_HUB_DISABLE_SYMLINKS_WARNING=1
SP="$HOME/ocrtest/scratchpad"
rm -rf ~/ocrtest/prep && mkdir -p ~/ocrtest/prep && cd ~/ocrtest/prep
cp "$SP/ocr_benchmark_src.py" ocr_benchmark.py
sed -i 's/^N_AMOSTRA = 60.*/N_AMOSTRA = 50/' ocr_benchmark.py
if [ -n "$EXCLUIR" ]; then sed -i "s/^EXCLUIR_IDS = set()/EXCLUIR_IDS = {$EXCLUIR}/" ocr_benchmark.py; fi
grep -nE "^N_AMOSTRA|^EXCLUIR_IDS" ocr_benchmark.py
~/ocrtest/py/bin/python $SP/prep_montage.py ocr_benchmark.py $SP/montagem 2>&1 | grep -v -i warn
