# Ficha de extração: 7 artigos marcados "Ler texto completo"

Fonte dos dados: **apenas resumos e metadados** (páginas das revistas e resultados de busca). Nenhum texto completo foi lido. "Não informado" significa que o resumo não traz a informação, não que o artigo não a tenha. Confira cada item no PDF antes de citar. As decisões de inclusão são sua.

| # | Artigo | Ferramentas de OCR | Dataset e idioma | Métricas e resultado (do resumo) | Compara 2 ou mais ferramentas? | Sugestão preliminar |
|---|---|---|---|---|---|---|
| 1 | Kotzé e Wolff (2020), *Exchanging image processing and OCR components in a Setswana digitisation pipeline*, South African Computer Journal 32(2) | Calamari (rede neural por linha) e Tesseract 3, com ImageMagick e Unpaper no pré-processamento | Documentos em setswana; nome e tamanho não informados | CER médio de 1,69 com ImageMagick/Unpaper e Calamari, mais de 30% melhor que a linha de base com Tesseract 3 | **Sim (2 motores)** | Incluir, se o texto completo confirmar métricas e dataset. Idioma diferente do português |
| 2 | Sugiarto e Santosa (2024), *Comparison of Thresholding Otsu and Morphology Opening Preprocessor... Using Tesseract*, Proxies 5(2) | Só Tesseract (versão não informada) | Não informado | Sem métrica nem número no resumo. A página é inconsistente: o título cita "morphology opening", o resumo cita dilatação | Não (compara pré-processamentos) | Excluir (E3), mas pode embasar a escolha de pré-processamento |
| 3 | Rawat et al. (2021), *Analysis of Image Preprocessing Techniques to Improve OCR of Garhwali Text...*, ICTACT J. Image and Video Processing 12(2) | Só Tesseract (modelo hindi) | 5 livros didáticos impressos em garhwali, fotografados com duas câmeras; total de imagens não informado | Acurácia (nível não informado): 88,13% (alta resolução, Otsu, sem super-resolução) e 87,44% (baixa resolução, ImageMagick e super-resolução). Sem linha de base sem pré-processamento | Não (compara pipelines de pré-processamento) | Excluir (E3), útil para discutir resolução e pré-processamento |
| 4 | Lech e Okarma (2015), *Prediction of the OCR Accuracy based on the Combined Assessment of Image Binarization Results*, Elektronika ir Elektrotechnika 21(6) | Só Tesseract | Imagens degradadas; dataset não informado | Propõe métrica combinada para prever a acurácia; sem números no resumo | Não (propõe métrica) | Excluir (E2) |
| 5 | Clausner et al. (2020), *Efficient and effective OCR engine training*, IJDAR 23(1) | Tesseract (estudo de caso de treinamento no Aletheia) | Dois datasets históricos de projetos de digitalização; detalhes não informados | Não informado no que consegui ver | Não (propõe fluxo de treinamento) | Excluir (E2) |
| 6 | Arslan (2022), *End to End Invoice Processing Application Based on Key Fields Extraction*, IEEE Access 10 | **O resumo não menciona OCR** | Não informado | YOLOv5 superou o processamento de imagens na detecção de tabelas | Não confirmado | Dúvida, tende a excluir (E4). Confirmar no texto completo se há comparação de OCR |
| 7 | Fateh et al. (2023), *Enhancing optical character recognition: Efficient techniques for document layout analysis and text line detection*, Engineering Reports 6(9) | Não é comparação de motores | Texto impresso em persa; propõe um dataset novo | Aprendizado profundo com votação, correção de ângulo e remoção de curvatura de linha | Não (propõe métodos) | Excluir (E2) |

## O que isso significa para a revisão
- Dos 7, **só 1 (Kotzé e Wolff) parece atender** ao critério de comparar 2 ou mais ferramentas com métrica.
- Os artigos 2, 3 e 4 são sobre pré-processamento. Servem como apoio ao método (por que testar ruído, resolução e binarização), não como estudos incluídos.
- O conjunto do CAPES, sozinho, não sustenta a revisão. O núcleo precisa vir dos estudos comparativos achados na web e das buscas nas bases.

## Falhas na coleta
- Springer (Clausner): pede login. IEEE Xplore (Arslan): página vazia. Wiley (Fateh): bloqueio 403. Nesses casos usei resultados de busca (DOAJ, repositórios), que mostram só parte do resumo.
- A página inicial de Kotzé e Wolff devolveu um conteúdo errado ("AST-Hints"). O resumo acima vem de uma busca e está parafraseado, então confira no [site da revista](https://sacj.cs.uct.ac.za/index.php/sacj/article/view/707).
- Na busca por Kotzé e Wolff apareceu também o arXiv 2608.24976, *A Comparative Evaluation of Digitization Pipelines for Historiographical Sources*. Não foi aberto, e vale checar como candidato.
