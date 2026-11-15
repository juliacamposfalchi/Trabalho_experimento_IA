import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

fig, ax = plt.subplots(figsize=(13, 9.5), dpi=200)
ax.set_xlim(0, 100); ax.set_ylim(-12, 100); ax.axis("off")

AZUL, CINZA, VERDE = "#DCE9F7", "#EFEFEF", "#DDF0DC"

def caixa(x, y, w, h, texto, cor=AZUL, fs=8.4, bold=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.25,rounding_size=0.8",
                                fc=cor, ec="#333333", lw=1))
    ax.text(x + w / 2, y + h / 2, texto, ha="center", va="center", fontsize=fs,
            fontweight="bold" if bold else "normal", linespacing=1.4)

def seta(x1, y1, x2, y2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color="#333333", lw=1.1))

for y, t in [(87, "Identificação"), (60, "Triagem"), (33, "Elegibilidade"), (11, "Inclusão")]:
    ax.add_patch(FancyBboxPatch((0.5, y - 8), 4, 16, boxstyle="round,pad=0.1", fc="#555555", ec="none"))
    ax.text(2.5, y, t, rotation=90, ha="center", va="center", color="white", fontsize=9, fontweight="bold")

# colunas: esquerda (base), meio (exclusões da base), direita (busca complementar)
LX, LW = 8, 32
MX, MW = 44, 30
RX, RW = 78, 20

# Identificação
caixa(LX, 80, LW, 14, "Registros identificados na base\nPeriódicos CAPES, 3 buscas\n10/11/2026\n(n = 76)")
caixa(RX, 80, RW, 14, "Relatos identificados na\nbusca complementar (web\ne arXiv), não sistemática\n(n = 5)", cor=CINZA, fs=8)
caixa(MX, 80, MW, 14, "Duplicados removidos\n(n = 7)", cor=CINZA)
seta(LX + LW, 87, MX, 87)

# Triagem
caixa(LX, 52, LW, 14, "Registros triados pelo título\n(resumo ausente nas exportações)\n(n = 69)")
seta(LX + LW / 2, 80, LX + LW / 2, 66)
caixa(MX, 46, MW, 26,
      "Excluídos na triagem (n = 62)\n\nFora do tema (E5): 29\nUma única ferramenta (E3): 18\nModelo sem comparação (E2): 7\nPós-correção, legenda ou\ndetecção (E4): 7\nManuscrito (E1): 1",
      cor=CINZA, fs=8.2)
seta(LX + LW, 59, MX, 59)

# Elegibilidade
caixa(LX, 24, LW, 14, "Registros avaliados em detalhe\n(resumo e metadados;\ntexto completo não lido)\n(n = 7)")
seta(LX + LW / 2, 52, LX + LW / 2, 38)
caixa(MX, 18, MW, 20,
      "Excluídos após avaliação (n = 6)\n\nSó Tesseract, pré-processamento\nou métrica (E3, E2): 3\nFluxo de treinamento ou\nmétodo novo (E2): 2\nResumo sem OCR (E4): 1",
      cor=CINZA, fs=8.2)
seta(LX + LW, 31, MX, 31)

caixa(RX, 22, RW, 16, "Relatos avaliados (n = 5)\n\nExcluído (n = 1): tradução\nde imagens com texto (E4)", cor=CINZA, fs=8)
seta(RX + RW / 2, 80, RX + RW / 2, 38)

# Inclusão
caixa(LX, 1, LW, 15, "Incluídos vindos da base\n(n = 1)\nKotzé e Wolff (2020)", cor=VERDE)
seta(LX + LW / 2, 24, LX + LW / 2, 16)
caixa(MX, -10, MW, 8, "Total de estudos incluídos\nna revisão (n = 5)", cor=VERDE, bold=True)
caixa(RX - 4, 1, RW + 4, 15, "Incluídos vindos da busca\ncomplementar (n = 4)\nKapelinski; Nagayi;\nFeng; Gómez Rey", cor=VERDE, fs=8)
seta(RX + RW / 2, 22, RX + RW / 2, 16)
seta(LX + LW / 2, 1, MX + 6, -2)
seta(RX + RW / 2 - 2, 1, MX + MW - 6, -2)

ax.set_title("Fluxo PRISMA 2020 da revisão parcial da literatura", fontsize=12, fontweight="bold", pad=8)
fig.savefig(r"C:/Users/julia.falchi/Downloads/Mestrado Qualificação/prisma_fluxo.png", bbox_inches="tight", facecolor="white")
print("ok")
