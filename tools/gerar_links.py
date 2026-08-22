#!/usr/bin/env python3
"""Gera os botoes de perfil do rodape do README, nos dois temas.

    python3 tools/gerar_links.py

Sai um SVG por botao e por tema em `assets/`, tipo `btn-linkedin-dark.svg`.

POR QUE UM ARQUIVO POR BOTAO, e nao uma fileira so. Link dentro de SVG embutido
como `<img>` e inerte, o navegador nao navega. Para cada botao ser clicavel, cada
um precisa ser a sua propria imagem, envolvida por um `<a>` no markdown. Fileira
unica ficaria bonita e morta.

DE ONDE VEM O TRACADO. `content/marcas-sociais.ts` do lucas-falcao-site, que ja
carrega os avisos de procedencia. Dois pontos herdados de la:

- LINKEDIN foi REMOVIDO do Simple Icons por politica de marca da propria
  LinkedIn, nao por proibicao de uso. O tracado e o "in" canonico, apontando
  para o perfil do Falcao NA LinkedIn, que e uso nominativo.
- LATTES nao tem marca vetorial distribuida, nem como Lattes nem como CNPq. Por
  isso sai como MONOGRAMA "Lt", e nao com logo emprestado. Mesma regra das
  fileiras de stack, o que nao tem marca propria nao recebe uma dos outros.

Site e e-mail nao sao marca de ninguem, sao funcao. Por isso o globo e o
envelope sao desenhados aqui mesmo, com primitiva geometrica.
"""
import json
from pathlib import Path

TEMAS = {
    "dark":  dict(icone="#aab3c9", borda="#1f2436", fundo="#10131f"),
    "light": dict(icone="#35425e", borda="#d7e0f2", fundo="#ffffff"),
}

LADO = 46
RAIO = 11
ICONE = 21
MONO = "ui-monospace,SFMono-Regular,SF Mono,Menlo,Consolas,Liberation Mono,monospace"

MARCAS = json.loads(Path(__file__).with_name("marcas-sociais.json").read_text(encoding="utf-8"))

# globo e envelope desenhados aqui, em viewBox 24, para casar com o resto
GLOBO = ("M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zm0 0c-2.5 2.4-3.8 5.6-3.8 10"
         "S9.5 19.6 12 22m0-20c2.5 2.4 3.8 5.6 3.8 10S14.5 19.6 12 22M2.6 9h18.8M2.6 15h18.8")
ENVELOPE = "M3 6h18v12H3zM3 6l9 7 9-7"

BOTOES = [
    ("site",     dict(tracado=GLOBO, preenche=False)),
    ("linkedin", dict(tracado=MARCAS["LinkedIn"], preenche=True)),
    ("instagram", dict(tracado=MARCAS["Instagram"], preenche=True)),
    ("lattes",   dict(monograma="Lt")),
    ("orcid",    dict(tracado=MARCAS["ORCID"], preenche=True)),
    ("email",    dict(tracado=ENVELOPE, preenche=False)),
]


def gerar(nome, spec, tema):
    c = TEMAS[tema]
    if "monograma" in spec:
        dentro = (f'<text x="{LADO/2}" y="{LADO/2 + 5.5:.1f}" text-anchor="middle"'
                  f' font-family="{MONO}" font-size="15" font-weight="500"'
                  f' fill="{c["icone"]}">{spec["monograma"]}</text>')
    else:
        esc = ICONE / 24
        d = (f'<path d="{spec["tracado"]}" fill="{c["icone"]}"/>' if spec["preenche"]
             else f'<path d="{spec["tracado"]}" fill="none" stroke="{c["icone"]}"'
                  f' stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>')
        dentro = (f'<g transform="translate({(LADO - ICONE)/2:.1f},{(LADO - ICONE)/2:.1f})'
                  f' scale({esc:.4f})">{d}</g>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {LADO} {LADO}"'
            f' width="{LADO}" height="{LADO}" role="img" aria-label="{nome}">'
            f'<rect x="0.75" y="0.75" width="{LADO-1.5}" height="{LADO-1.5}" rx="{RAIO}"'
            f' fill="{c["fundo"]}" stroke="{c["borda"]}" stroke-width="1.5"/>{dentro}</svg>\n')


if __name__ == "__main__":
    destino = Path(__file__).resolve().parent.parent / "assets"
    destino.mkdir(exist_ok=True)
    for nome, spec in BOTOES:
        for tema in TEMAS:
            alvo = destino / f"btn-{nome}-{tema}.svg"
            alvo.write_text(gerar(nome, spec, tema), encoding="utf-8")
    print(f"{len(BOTOES) * len(TEMAS)} botoes gerados")
