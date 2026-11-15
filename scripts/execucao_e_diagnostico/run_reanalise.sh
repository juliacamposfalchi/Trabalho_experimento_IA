#!/bin/bash
export PYTHONNOUSERSITE=1 PYTHONIOENCODING=utf-8
cd ~/ocrtest/work || exit 1
~/ocrtest/py/bin/python "$HOME/ocrtest/scratchpad/reanalise_caixa.py"
