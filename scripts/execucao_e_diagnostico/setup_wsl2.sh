#!/bin/bash
set -e
cd ~/ocrtest
echo "== python 3.12 via micromamba =="
./bin/micromamba create -y -q -p ~/ocrtest/py -c conda-forge python=3.12 pip
PIP=~/ocrtest/py/bin/pip
$PIP install -q --upgrade pip
echo "== torch CPU =="
$PIP install -q torch torchvision --index-url https://download.pytorch.org/whl/cpu
echo "== demais pacotes =="
$PIP install -q pytesseract easyocr "python-doctr[torch]" paddleocr paddlepaddle jiwer opencv-python-headless pandas matplotlib scipy datasets pillow
$PIP list 2>/dev/null | grep -iE "^(torch|easyocr|paddleocr|paddlepaddle|python-doctr|pytesseract|jiwer|datasets) "
echo "== SETUP_OK =="
