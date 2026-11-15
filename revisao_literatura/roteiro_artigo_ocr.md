# Roteiro de escrita: artigo de comparação de OCR (máx. 20 páginas)

Este arquivo NÃO contém texto do artigo. São perguntas-guia e espaços de evidência para você escrever cada seção com a sua voz. Quando tiver um parágrafo, cole no chat para revisão.

## Orçamento de páginas
| Seção | Páginas |
|---|---|
| Resumo e palavras-chave | 0,5 |
| 1. Introdução | 2 |
| 2. Revisão da literatura (PRISMA) | 4 a 5 |
| 3. Método | 4 |
| 4. Resultados | 3 a 4 |
| 5. Discussão e limitações | 2 |
| 6. Conclusão | 1 |
| Referências | 1 a 2 |

## Lembretes do seu estilo (da dissertação)
- Abrir pelo contexto geral e estreitar até o problema.
- Estrutura do parágrafo: contexto, dificuldade ("Entretanto", "Apesar de"), consequência ("torna-se pertinente").
- Voz impessoal: "Busca-se", "Espera-se", "Observa-se que".
- Hipótese, questão principal, questões derivadas (a, b, c) e objetivos com verbo no infinitivo.
- Delimitar o que o trabalho não é.
- Termos em inglês em itálico, com a sigla entre parênteses na primeira vez.

## 1. Introdução
Perguntas que cada parágrafo responde:
1. Por que extrair texto de imagens é relevante hoje (que tipo de documento, que uso)?
2. Qual a dificuldade? (muitas ferramentas, resultados variam com o tipo de documento e a qualidade da imagem)
3. O que a literatura já fez? (cite 2 ou 3 comparações: arXiv 2510.03570, arXiv 2602.02223, Reading Brazil / ENIAC 2026)
4. Qual a lacuna específica? ATENÇÃO: já existe comparação em documentos brasileiros (Reading Brazil, 14 motores). Sua lacuna precisa ser mais estreita. Opções para você escolher:
   - Quatro ferramentas amplamente usadas, sob degradações controladas e reprodutíveis;
   - Foco em custo computacional (tempo, memória) além do erro;
   - Dataset e código abertos para replicação por estudantes.
   RECORTE ESCOLHIDO (decisão da Julia): CER e WER (o Reading Brazil usa NED e FVR) em cenário só com CPU, com versões fixas, código aberto e testes estatísticos pareados. Posicionar o trabalho como replicação parcial e extensão do Reading Brazil (ENIAC 2026). A hipótese e os objetivos precisam refletir esse recorte e ser escritos por você.
5. Qual a sua hipótese, a questão principal, as questões derivadas e os objetivos?
6. Como o artigo está organizado?

Escreva você: hipótese (1 frase testável, com métrica e condição), questão principal (1 pergunta), objetivos (verbos no infinitivo).

## 2. Revisão da literatura (PRISMA parcial)
Espaços de evidência (preencha com os dados reais, depois de ler os artigos):
- Busca: bases, strings, datas, número de registros por base.
- Fluxo: identificados (76 nos exports do CAPES, 69 sem duplicados), triados, elegíveis, incluídos.
- Critérios de inclusão e exclusão (use os da conversa anterior).
- Quadro de síntese por artigo: ferramentas, dataset, idioma, métricas, achado principal.
Perguntas-guia:
1. O que os estudos incluídos têm em comum (ferramentas, métricas)?
2. Onde divergem e por quê (domínio, idioma, resolução)?
3. Que tipo de dataset foi usado? Algum em português?
4. O que ficou sem resposta (a lacuna da seção 1, agora com evidência)?
Cuidado: não use estudos de aplicação (placas de veículos etc.) como se fossem comparação.

## 3. Método
Decisões que você precisa tomar e justificar:
- Dataset (ex.: DharmaOCR-Benchmark, partes impressas; ESTER-Pt): tamanho, licença, como o texto de referência foi obtido.
- Ferramentas e versões exatas (Tesseract, EasyOCR, PaddleOCR, docTR; considerar Surya).
- Normalização do texto antes de medir (espaços, acentos, caixa).
- Métricas: CER, WER, tempo por imagem, ambiente (CPU ou GPU, hardware).
- Condições: original, ruído, rotação, baixa resolução (parâmetros usados).
- Aquecimento e repetições (para o tempo).
- Disponibilização: repositório no GitHub com `ocr_benchmark.py`, dados e resultados.
Fórmulas de CER e WER devem aparecer no texto (distância de edição dividida pelo tamanho da referência).

## 4. Resultados
Só descrever o que a tabela mostra, sem interpretar:
- Tabela principal: CER e WER médios (com desvio) por ferramenta e condição.
- Tabela de tempo por ferramenta.
- Gráfico de CER por condição (gerado pelo script).
- Teste estatístico simples (ex.: Wilcoxon pareado) se for afirmar que uma ferramenta é melhor.

## 5. Discussão e limitações
1. A hipótese foi confirmada, refutada ou parcialmente confirmada? Com base em quê?
2. Como os resultados se comparam com a literatura da seção 2?
3. Por que algumas ferramentas pioram mais com ruído ou rotação?
4. Limitações obrigatórias: tamanho e tipo do dataset, documentos sintéticos ou jurídicos, versões das ferramentas, hardware, sem ajuste fino, vocabulário do docTR e acentos.
5. O que o trabalho não conclui (delimitação).

## 6. Conclusão
- Responder à questão principal em 1 parágrafo.
- Contribuição (código e dados abertos, protocolo reprodutível).
- Trabalhos futuros (mais ferramentas, VLMs, mais tipos de documento).

## Uso de IA (regra da disciplina)
Declare no artigo, se a professora exigir, que a IA foi usada para auxiliar o código e para revisar o texto, e que a redação é sua.
