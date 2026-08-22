#!/usr/bin/env python3
"""Gera o carrossel de stack do README, agrupado por objetivo, nos dois temas.

    python3 tools/gerar_stack.py

Sai `assets/stack-dark.svg` e `assets/stack-light.svg`.

DUAS FILEIRAS LONGAS, EM SENTIDOS OPOSTOS, so com as marcas. O rotulo da
categoria saiu a pedido do Falcao, mas a ORDEM continua agrupada por objetivo:
linguagem, framework e banco na primeira esteira, dado, ia e orquestracao na
segunda. O vao entre os chips e uniforme de proposito; sem rotulo, um vao maior
separando grupo leria como falha de espacamento, e nao como divisao.

A primeira tentativa foi uma fileira por categoria, com o rotulo parado a
esquerda. Ficou ruim por um motivo de aritmetica: com trinta chips divididos em
seis, cada fileira mede menos que a janela, entao o laco aparecia repetindo na
tela, e `orchestration/`, que tem dois itens, virava
"Docker Kubernetes Docker Kubernetes Docker". Carrossel so funciona quando o
conteudo transborda MUITO a janela.

Juntando em duas esteiras de quinze, cada uma passa de mil e quinhentos pixels
contra novecentos de janela, entao a volta nunca aparece inteira e a repeticao
some. E como o rotulo anda colado no seu proprio grupo, a organizacao por
objetivo continua de pe, que era o ponto.

O LACO E COSTURADO, NAO CORTADO. A sequencia de chips e repetida ate cobrir mais
de duas vezes a janela, e o deslocamento anda exatamente a largura de UMA
sequencia. Quando a animacao reinicia, o quadro seguinte e identico ao anterior,
entao nao existe salto. Repetir de menos e o erro classico, deixa buraco no fim
da volta.

AS PONTAS SAO ESMAECIDAS por mascara com degrade. Sem isso o chip aparece e some
cortado ao meio na borda da janela, que le como falha de render.

DE ONDE VEM O TRACADO. Simple Icons (github.com/simple-icons/simple-icons), sob
CC0, o mesmo conjunto que `content/stack-marcas.ts` do lucas-falcao-site usa. Os
caminhos ficam embutidos aqui de proposito, o README nao pode depender de CDN.

As marcas sao de seus donos e aparecem em uso nominativo, so para identificar a
tecnologia. Renderizam monocromaticas, porque logo colorido quebra a paleta.

CHIP SEM MARCA E NORMAL. SQL, statsmodels, Matplotlib, seaborn e Llama nao tem
icone proprio no conjunto. Entram so com o nome, e nao com logo emprestado de
coisa parecida. Regra herdada do site, icone e enfeite de quem tem, e pegar a
marca do vizinho seria afirmar ferramenta que nao foi usada.
"""
import json
from pathlib import Path
from xml.sax.saxutils import escape

TEMAS = {
    "dark":  dict(rotulo="#4d7cff", icone="#8fb0ff", texto="#aab3c9",
                  chip="#10131f", borda="#1f2436", fundo="#0d1117"),
    "light": dict(rotulo="#2f5fe0", icone="#2563eb", texto="#35425e",
                  chip="#ffffff", borda="#d7e0f2", fundo="#ffffff"),
}

MONO = "ui-monospace,SFMono-Regular,SF Mono,Menlo,Consolas,Liberation Mono,monospace"
W = 900
COL = 172          # onde a janela do carrossel comeca
MARGEM = 8         # respiro na ponta direita
ALT_CHIP = 30
FILEIRA = 46
ICONE = 16
FONTE = 11.5
AVANCO = 0.6
VAO = 9            # entre um chip e o proximo
PAD = 9            # respiro interno do chip
VELOCIDADE = 34    # pixels por segundo

DADOS = json.loads(Path(__file__).with_name("stack-dados.json").read_text(encoding="utf-8"))
GRUPOS = DADOS["grupos"]
TRACADOS = DADOS["tracados"]


def largura(nome, tem_icone):
    return PAD + (ICONE + 6 if tem_icone else 0) + len(nome) * FONTE * AVANCO + PAD


def chip(nome, slug, x, y, c):
    tx, dentro = x + PAD, ""
    if slug:
        dentro += (f'<g transform="translate({tx:.1f},{y + (ALT_CHIP - ICONE) / 2:.1f})'
                   f' scale({ICONE / 24:.4f})"><path d="{TRACADOS[slug]}" fill="{c["icone"]}"/></g>')
        tx += ICONE + 6
    dentro += (f'<text x="{tx:.1f}" y="{y + ALT_CHIP / 2 + 3.6:.1f}" font-family="{MONO}"'
               f' font-size="{FONTE}" fill="{c["texto"]}">{escape(nome)}</text>')
    return (f'<rect x="{x:.1f}" y="{y}" width="{largura(nome, bool(slug)):.1f}"'
            f' height="{ALT_CHIP}" rx="7" fill="{c["chip"]}" stroke="{c["borda"]}"/>{dentro}')


# As duas esteiras. A divisao busca larguras parecidas, para as voltas nao
# ficarem com duracoes muito diferentes uma da outra.
ESTEIRAS = [["languages/", "frameworks/", "databases/"],
            ["data/", "ai/", "orchestration/"]]


def gerar(tema):
    c = TEMAS[tema]
    por_nome = dict(GRUPOS)
    partes, y = [], 18
    for i, nomes in enumerate(ESTEIRAS):
        pecas, x = [], 0.0
        for rotulo in nomes:
            for nome, slug in por_nome[rotulo]:
                pecas.append(((nome, slug), x))
                x += largura(nome, bool(slug)) + VAO
        seq = x
        vezes = int(2 * W / seq) + 2
        conteudo = []
        for r in range(vezes):
            desloc = r * seq
            for (nome, slug), px in pecas:
                conteudo.append(chip(nome, slug, px + desloc, 0, c))
        dur = round(seq / VELOCIDADE, 2)
        vai = f"0 0;{-seq:.1f} 0" if i == 0 else f"{-seq:.1f} 0;0 0"
        partes.append(
            f'<g clip-path="url(#janela)" mask="url(#pontas)"><g transform="translate(0,{y})">'
            f'<g>{"".join(conteudo)}'
            f'<animateTransform attributeName="transform" type="translate" dur="{dur}s"'
            f' repeatCount="indefinite" calcMode="linear" values="{vai}"/></g></g></g>')
        y += FILEIRA
    H = y + 2
    todas = ", ".join(n for _, itens in GRUPOS for n, _ in itens)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Stack: {escape(todas)}">
<defs>
<clipPath id="janela"><rect x="0" y="0" width="{W}" height="{H}"/></clipPath>
<linearGradient id="fade" x1="0" x2="1">
  <stop offset="0" stop-color="#000"/><stop offset="0.05" stop-color="#fff"/>
  <stop offset="0.95" stop-color="#fff"/><stop offset="1" stop-color="#000"/>
</linearGradient>
<mask id="pontas"><rect x="0" y="0" width="{W}" height="{H}" fill="url(#fade)"/></mask>
</defs>
{"".join(partes)}
</svg>
'''


if __name__ == "__main__":
    destino = Path(__file__).resolve().parent.parent / "assets"
    destino.mkdir(exist_ok=True)
    for tema in TEMAS:
        alvo = destino / f"stack-{tema}.svg"
        alvo.write_text(gerar(tema), encoding="utf-8")
        print(f"{alvo.name}  {alvo.stat().st_size // 1024} KB")
