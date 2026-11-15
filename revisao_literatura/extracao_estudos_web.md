# Ficha de extração: estudos comparativos encontrados na web

Fontes: **Reading Brazil** foi lido no PDF (10 páginas de corpo, mais conclusão e referências). Os demais foram lidos pela página do arXiv (resumo, ou HTML no caso do 2510.03570), exceto onde indicado. Confira cada número no PDF antes de citar.

## 1. Reading Brazil (ENIAC 2026), o mais importante para você
Kapelinski, Lunkes, Welfer, Schmidt, Machado e Kreutz (UNIPAMPA e UFSM). DOI 10.5753/eniac.2026.31378. Código e gold: https://gitlab.com/cristhianavila.aluno/ocr-ptbr-benchmark

| Item | Dado |
|---|---|
| Motores | 14 abertos: 8 modelos de visão e linguagem (PaddleOCR-VL, HunyuanOCR, MinerU2.5, DeepSeek-OCR, dots.ocr, Qwen3-VL, Qwen2.5-VL, GLM-OCR) e 6 motores de OCR: **Tesseract, EasyOCR, docTR, RapidOCR, PaddleOCR e Surya** |
| Datasets | Formulários brasileiros (n=50, XFUND, gold reconstruído); documentos de identidade sintéticos (n=50, BRIDP); formulários em inglês como controle (n=30, FUNSD); **RIB**: 200 páginas literárias limpas do séc. XIX, ortografia pré-1911; **HYB**: 224 páginas degradadas (8 tipos sobre 28 páginas base). RIB e HYB vêm da suíte **ESTER-Pt** (Santos et al. 2023) |
| Degradações (HYB) | Bleed-through, blur, degradação de caracteres, furos, ruído gaussiano, sal e pimenta, fantasma e rotação |
| Métricas | FVR (recall de valores de campo) em formulários e IDs; NED em % (distância de edição normalizada) em prosa e degradadas; intervalos de 95% (bootstrap); **mediana do tempo por página** |
| Hardware | AMD Ryzen 7 9700X, 64 GB, RTX 5080 16 GB; motores clássicos no CPU, VLMs na GPU com vLLM; configurações padrão dos fabricantes |

Resultados que interessam (Tabelas 3, 4 e 5 do artigo):

| Motor | Formulários FVR | IDs FVR | Prosa limpa NED% | Degradadas NED% | Tempo por formulário (s) |
|---|---|---|---|---|---|
| Tesseract | 0,918 | 0,240 | 93,68 | 77,25 | 0,80 (CPU) |
| EasyOCR | 0,919 | 0,486 | 80,81 | 73,74 | 6,96 (CPU) |
| docTR | 0,898 | 0,822 | 90,43 | 79,96 | 1,84 (CPU) |
| PaddleOCR | 0,900 | 0,822 | 94,98 | 77,43 | 10,76 (CPU) |
| Surya | 0,965 | 0,921 | 96,67 | 93,89 | 5,88 (GPU) |

Por tipo de degradação (NED%): ruído sal e pimenta quebra todos os clássicos (Tesseract 0,8; EasyOCR 45,2; docTR 66,4; PaddleOCR 61,3). Rotação derruba Tesseract (48,2), EasyOCR (54,1) e docTR (49,3); PaddleOCR segura (79,1). O Tesseract é o melhor em ruído gaussiano (99,1) e em bleed-through (98,7).
Conclusões dos autores: nenhuma classe vence em tudo; só Surya e Qwen2.5-VL se sustentam nos quatro tipos de documento; a escolha deve seguir o tipo de documento; Tesseract e EasyOCR colapsam em fotos de identidade e em ruído e rotação.
Limitações declaradas: amostras de 50 documentos, gold dos formulários reconstruído por modelo multimodal (possível viés a favor dos VLMs), custo medido em uma única máquina, dois motores em fp8, sem medida de memória.
Código e dados: sim, no GitLab acima (gold liberado onde a licença permite).

**Impacto para o seu trabalho:** este artigo já fez, em português, a comparação de Tesseract, EasyOCR, docTR e PaddleOCR sob ruído, rotação, blur, e com tempo. Sua lacuna não pode ser "comparar essas ferramentas em português com degradações". Ela precisa ser outra (ver ideias no fim).

## 2. arXiv 2510.03570 (Nagayi et al., 2025), embalagens de alimentos na África do Sul
Fonte: HTML completo.
- Ferramentas: pytesseract 0.3.13, EasyOCR 1.7.2, PaddleOCR 2.7.0.3 (pipeline PP-OCRv5), TrOCR base-printed.
- Dataset: 1.628 imagens de 231 produtos (tempo e cobertura); acurácia em subconjunto transcrito de 113 imagens (60 produtos); texto multilíngue, idiomas não informados.
- Métricas: CER, WER, BLEU, ROUGE-L, F1, cobertura e tempo. Hardware: Intel 24 núcleos, 128 GB, RTX 3070; GPU para EasyOCR e TrOCR, CPU para Tesseract e PaddleOCR.
- CER médio: Tesseract 0,912; PaddleOCR 0,985; TrOCR 1,049; EasyOCR 1,075. WER: Tesseract 6,26; PaddleOCR 6,86; TrOCR 7,24; EasyOCR 7,41. Tempo médio por imagem: Tesseract 0,58 s; EasyOCR 0,81 s; TrOCR 2,20 s; PaddleOCR 6,24 s. Cobertura: PaddleOCR 98,3%; EasyOCR 91,5%; Tesseract 79,7%.
- Limitações (incluindo as que se vê no texto): acurácia em só 113 imagens; pré-processamento diferente entre ferramentas (só o Tesseract recebeu denoising e contraste); CER acima de 1,0 por inserções em textos curtos; PaddleOCR em CPU distorce a comparação de tempo; sem degradações controladas; modelos sem ajuste fino.
- Código e dados: não informados. É preprint.
- **Ponto de método para você:** use o mesmo pré-processamento para todas as ferramentas, senão a comparação não é justa.

## 3. arXiv 2602.02223 (Feng et al., 2026), tecnologia assistiva
Fonte: só a página do resumo.
- Ferramentas: Google Vision, PaddleOCR 3.0, EasyOCR e Tesseract (só o PaddleOCR tem versão informada).
- Condições: distância (1 a 7 m), ângulo (0 a 75 graus), velocidade de caminhada (0,8 a 1,8 m/s, só PaddleOCR), posição da câmera e tipo de câmera.
- Métrica: acurácia por caractere (razão de Levenshtein).
- Resultados (qualitativos, sem números no resumo): Google Vision foi o melhor; PaddleOCR foi o melhor entre os abertos; acurácia cai com movimento e ângulo maior.
- Dataset, hardware, limitações e código: não informados na página.
- Adequação aos critérios: compara 2 ou mais ferramentas com métrica, mas é um cenário de captura em movimento. Verificar no texto completo.

## 4. arXiv 2605.29476 (Puchol et al., 2026): **NÃO é comparação de OCR**
Compara sistemas de **tradução** de imagens com texto (pipelines modulares com docTR e LLMs, modelos multimodais e um modelo de ponta a ponta), com BLEU, chrF e TER. O resumo não menciona o EasyOCR.
**Correção:** na primeira busca, o resumo gerado dizia que este artigo mostrava docTR muito à frente do EasyOCR em CER (3 a 6% contra 12 a 18%). Isso **não está sustentado** pela página do artigo. Não use esses números. Excluir (E4).

## 5. arXiv 2608.24976 (Gómez Rey et al., 2026), pipelines de digitalização de fontes historiográficas
Fonte: só a página do resumo.
- 13 abordagens em três famílias (extração direta, pós-correção por LLM, extração por trechos). Só o Marker é nomeado; versões e o resto da lista não informados.
- Documentos: fontes secundárias sobre o período visigodo, em cinco categorias; idioma, tamanho e dataset não informados.
- Métricas: CER e WER contra gold corrigido à mão. Marker: 98,70% (CER) e 97,71% (WER) de acurácia geral.
- Conclusão: o parsing de documentos de ponta a ponta é o mais confiável; a pós-correção por LLM não traz ganho sistemático e frequentemente piora extrações corretas.
- Adequação: compara várias abordagens com CER e WER, mas não os motores clássicos. Candidato a incluir, depois de ver o texto completo.

## O que isso muda no seu artigo (ideias para você decidir, não texto)
1. A lacuna "comparação em português com degradações" já foi coberta pelo Reading Brazil. Opções de recorte que ainda são suas:
   - **Replicação e extensão com outro dataset e outras métricas:** usar o DharmaOCR (outras páginas, incluindo documentos jurídicos) e reportar **CER e WER**, que o Reading Brazil não usa (ele usa NED e FVR).
   - **Cenário só com CPU e configuração mínima**, para quem não tem GPU (estudantes, pequenas instituições), com versões fixas e código aberto.
   - **Sensibilidade ao pré-processamento** (binarização, redimensionamento) aplicada de forma igual a todas as ferramentas, dado que Sugiarto, Rawat e Lech tratam disso só com o Tesseract.
2. Inclua o **Surya** no experimento, porque foi o melhor motor de OCR do Reading Brazil.
3. O repositório deles (gold e código de avaliação) pode ser reaproveitado, citando a fonte e conferindo a licença.
4. Você pode declarar o trabalho como replicação parcial, o que é aceito e honesto, desde que a diferença esteja clara.
