#!/bin/bash
set -e
export PYTHONNOUSERSITE=1
PY=$HOME/ocrtest/py/bin/python
$PY -m pip install -q pytesseract easyocr "python-doctr[torch]" paddleocr paddlepaddle jiwer opencv-python-headless pandas matplotlib scipy datasets pillow numpy
$PY -c "import pandas, numpy, cv2, scipy, jiwer, torch, easyocr, doctr, paddleocr, pytesseract, datasets, PIL; print('imports ok')"
echo "== SETUP3_OK =="
