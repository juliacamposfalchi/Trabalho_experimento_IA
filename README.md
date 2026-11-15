# Comparação de ferramentas de OCR de código aberto em CPU para documentos em português

Experimento e revisão parcial da literatura (PRISMA) sobre Tesseract, EasyOCR, PaddleOCR e docTR em 40 páginas
em português do DharmaOCR-Benchmark, na condição original e com quatro degradações (ruído gaussiano, sal e pimenta,
rotação de 5 graus e redução de resolução). Métricas: CER e WER (e versões sem distinção de maiúsculas), tempo por
página, intervalos de confiança por bootstrap e testes de Wilcoxon pareados.

## Estrutura

| Pasta/arquivo | Conteúdo |
|---|---|
| `scripts/ocr_benchmark.py` | Experimento principal (amostragem, degradações, execução das ferramentas, métricas, testes) |
| `scripts/reanalise_caixa.py` | Reanálise secundária sem distinção de maiúsculas |
| `scripts/execucao_e_diagnostico/` | Scripts auxiliares de execução, instalação no WSL e diagnóstico |
| `dados/` | 40 páginas (`imagens/`), transcrições de referência (`referencias/`) e `manifest.csv` |
| `resultados_40pag/` | CSVs de resultados, resumos, testes, gráfico e as 800 saídas de OCR (`hipoteses/`) |
| `revisao_literatura/` | Protocolo, exportações do Periódicos CAPES, fichas de extração, scripts da triagem e do PRISMA |
| `triagem_prisma_ocr.xlsx` | Planilha com toda a triagem, o PRISMA e os resultados |
| `prisma_fluxo.png` | Diagrama PRISMA |
| `artigo_ocr_rascunho.txt` | Rascunho do artigo |
| `logs/` | Registros das execuções |

## Ambiente do experimento
Intel Core Ultra 7 165U (14 threads lógicos), 31,4 GB de RAM (23 GB visíveis ao WSL2), sem GPU, Windows 11 com
WSL2 (Ubuntu 24.04), Python 3.12.16. Versões: Tesseract 5.5.3 (pytesseract 0.3.13), EasyOCR 1.7.2,
PaddleOCR 3.7.0 (paddlepaddle 3.3.1), docTR 1.1.0, jiwer 4.0.0. Semente: 42. Detalhes em `resultados_40pag/ambiente.json`.

## Observações
- Os scripts usam caminhos do ambiente original (`~/ocrtest/work`); ajuste antes de rodar.
- As imagens e referências vêm do DharmaOCR-Benchmark e seguem a licença do conjunto original.
- Parâmetros de degradação foram escolhidos diretamente, sem calibração.
- As colunas de decisão da triagem foram preenchidas com apoio de IA, a partir de título, resumo e metadados, e precisam de conferência.
