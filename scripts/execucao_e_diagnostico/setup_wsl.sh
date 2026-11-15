#!/bin/bash
set -e
mkdir -p ~/ocrtest && cd ~/ocrtest
echo "== micromamba + tesseract (conda-forge) =="
if [ ! -x bin/micromamba ]; then
  curl -Ls https://micro.mamba.pm/api/micromamba/linux-64/latest | tar -xj bin/micromamba
fi
./bin/micromamba create -y -q -p ~/ocrtest/mm -c conda-forge tesseract
mkdir -p tessdata
curl -sL -o tessdata/por.traineddata https://github.com/tesseract-ocr/tessdata_fast/raw/main/por.traineddata
ls -la tessdata
~/ocrtest/mm/bin/tesseract --version 2>&1 | head -2
echo "== venv + pacotes python (torch CPU) =="
python3 -m venv venv
venv/bin/pip install -q --upgrade pip
venv/bin/pip install -q torch torchvision --index-url https://download.pytorch.org/whl/cpu
venv/bin/pip install -q pytesseract easyocr "python-doctr[torch]" paddleocr paddlepaddle jiwer opencv-python-headless pandas matplotlib scipy datasets pillow
venv/bin/pip list 2>/dev/null | grep -iE "^(torch|easyocr|paddleocr|paddlepaddle|python-doctr|pytesseract|jiwer|datasets) "
echo "== SETUP_OK =="
