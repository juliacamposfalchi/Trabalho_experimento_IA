# Protocolo da revisão sistemática (parcial, PRISMA) sobre comparação de ferramentas de OCR

Este é um protocolo de trabalho (o plano da busca e da triagem). A escrita da seção de revisão do artigo é sua. Registre as datas e os números reais de cada etapa, porque o diagrama PRISMA depende deles.

## 1. Pergunta de pesquisa
Como as ferramentas de OCR de código aberto (Tesseract, EasyOCR, PaddleOCR, docTR e similares) se comparam em acurácia (CER, WER) e custo computacional na extração de texto de imagens de documentos?
Sub-perguntas:
- RQ1. Que ferramentas e métricas os estudos comparativos utilizam?
- RQ2. Em que tipos de documento e idiomas a comparação foi feita? Há estudos em português?
- RQ3. Que fatores (ruído, resolução, rotação, pré-processamento) afetam o desempenho?
- RQ4. Que lacunas permanecem?

## 2. Bases e strings (testar uma por uma e ajustar)
Lição da primeira tentativa: strings longas retornaram zero no CAPES, e "OCR" casou com "ocrelizumab". Restrinja ao título, resumo e palavras-chave e use poucos blocos. A sintaxe de cada base pode diferir, então confira na ajuda da base e registre a string exata que rodou.

| Base | String sugerida (inglês) |
|---|---|
| Web of Science | `TS=(("optical character recognition" OR OCR) AND (Tesseract OR EasyOCR OR PaddleOCR OR docTR OR TrOCR OR Surya) AND (compar* OR benchmark* OR evaluat*))` |
| Scopus | `TITLE-ABS-KEY(("optical character recognition" OR OCR) AND (Tesseract OR EasyOCR OR PaddleOCR OR docTR OR TrOCR) AND (compar* OR benchmark* OR evaluat*))` e filtro de ano |
| IEEE Xplore | `("optical character recognition" OR OCR) AND (Tesseract OR EasyOCR OR PaddleOCR) AND (comparison OR benchmark OR evaluation)` em "Abstract" |
| ACM Digital Library | mesma lógica, em título e resumo |
| arXiv | `all:OCR AND (all:Tesseract OR all:EasyOCR OR all:PaddleOCR)` |
| SciELO / BDTD / SBC OpenLib | `("reconhecimento óptico de caracteres" OR OCR) AND (comparação OR avaliação OR Tesseract)` |
| CAPES | usar busca avançada, campo "título" ou "assunto", e strings curtas |
| Complemento | Google Scholar (primeiras 100 a 200 entradas) e busca em bola de neve (referências dos artigos incluídos) |

Para cada base, anote: data da busca, string exata, filtros, número de resultados e número exportado.

## 3. Critérios de elegibilidade
Inclusão:
- 2018 a 2026;
- compara duas ou mais ferramentas ou motores de OCR;
- reporta métrica quantitativa (CER, WER, acurácia, tempo ou custo);
- imagens de documentos ou de texto impresso (cenas também, se a comparação for de motores);
- inglês ou português; texto completo acessível.
Exclusão:
- manuscrito (HTR) como foco;
- propõe um modelo novo sem comparar com outras ferramentas;
- aplicação de uma única ferramenta (ex.: Tesseract em placas de veículos) sem comparação;
- pós-correção, legendagem de imagens ou detecção de texto sem avaliação de reconhecimento;
- duplicados e versões repetidas do mesmo estudo.

## 4. Processo de seleção
1. Exportar tudo (BibTeX ou RIS) e unir em uma planilha única, com uma coluna para a base de origem.
2. Remover duplicados (por DOI e por título normalizado) e registrar quantos.
3. Triagem por título e resumo (decisão: incluir, excluir, dúvida; com motivo).
4. Leitura do texto completo dos que sobraram (decisão final e motivo, usando os códigos E1 a E6 dos critérios de exclusão).
5. Se possível, uma segunda pessoa confere uma amostra da triagem (ou você refaz 10% depois de alguns dias) e você relata a concordância.

## 5. Ficha de extração (uma linha por estudo incluído)
Referência, ano, tipo de publicação, ferramentas comparadas (com versões), dataset (nome, tamanho, idioma, tipo de documento), pré-processamento, degradações testadas, métricas, hardware, principal resultado (número), conclusão dos autores, limitações, código ou dados abertos (sim ou não).

## 6. Avaliação de qualidade e risco de viés (versão simples)
Para cada estudo: o dataset é descrito? A referência (ground truth) é descrita? As versões das ferramentas são informadas? O protocolo é reproduzível (código ou dados)? As métricas são definidas? Marque sim, parcial ou não, e use isso na discussão (não necessariamente para excluir).

## 7. Registro PRISMA (preencher)
| Etapa | Número |
|---|---|
| Registros identificados por base | ___ |
| Registros após remover duplicados | ___ (CAPES atual: 76 identificados, 69 sem duplicados) |
| Triados por título e resumo | ___ |
| Excluídos na triagem | ___ |
| Textos completos avaliados | ___ |
| Excluídos com motivo (E1 a E6) | ___ |
| Estudos incluídos | ___ |

## 8. Sementes já identificadas (verificar e ler por inteiro)
- Reading Brazil (ENIAC 2026): 14 motores em documentos brasileiros.
- arXiv 2510.03570: Tesseract, EasyOCR, PaddleOCR e TrOCR em embalagens.
- arXiv 2602.02223: PaddleOCR 3.0, Tesseract, EasyOCR e Google Vision, em tecnologia assistiva.
- arXiv 2605.29476: docTR e EasyOCR em imagens com texto.
- Sugiarto e Santosa (2024), Kotzé e Wolff (2020), Rawat et al. (2021): pré-processamento e componentes de OCR (do CAPES, verificar elegibilidade).

## 9. Limitações já previstas (para a seção de limitações do artigo)
Revisão parcial (poucas bases, uma pessoa revisando), busca restrita a inglês e português, literatura cinzenta (blogs, páginas de fornecedores) fora do conjunto incluído, e possível viés de publicação.
