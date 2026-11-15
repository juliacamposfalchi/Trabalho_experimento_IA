#!/bin/bash
export PYTHONNOUSERSITE=1 PYTHONIOENCODING=utf-8 HF_HUB_DISABLE_SYMLINKS_WARNING=1
export TESSDATA_PREFIX=$HOME/ocrtest/tessdata
export PATH=$HOME/ocrtest/mm/bin:$PATH
SP="$HOME/ocrtest/scratchpad"
echo "== analise do teste =="; ~/ocrtest/py/bin/python "$SP/analisa_teste.py" 2>&1 | grep -v Warning
echo; echo "== diagnostico Tesseract: tamanho original contra 2000 px =="; ~/ocrtest/py/bin/python $SP/diagnostico.py 2>&1 | grep -v -i warn
