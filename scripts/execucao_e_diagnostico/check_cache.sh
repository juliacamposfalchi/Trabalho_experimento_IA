#!/bin/bash
for d in ~/.EasyOCR/model ~/.cache/doctr ~/.paddlex ~/.cache/huggingface/hub ~/ocrtest/tessdata; do
  if [ -d "$d" ]; then echo "OK    $d  $(du -sh "$d" | cut -f1)"; else echo "FALTA $d"; fi
done
