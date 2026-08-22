#!/usr/bin/env python3
"""Gera o README a partir de `textos.py`.

    python3 tools/gerar_readme.py

Sai `README.md`, em ingles.

⚠ O SELETOR DE IDIOMA FOI DESCARTADO. O motivo esta escrito em `textos.py`, e o
resumo e que a pagina do perfil serve sempre o `README.md`, entao bandeira
clicavel jogaria o visitante fora do perfil, longe do grafico e dos repos fixados.

POR QUE GERAR E NAO ESCREVER A MAO. Quatro textos escritos a mao divergem na
primeira correcao, e o README de um idioma passa a dizer algo que o outro nao diz.
Com dicionario existe uma fonte de verdade e um comando.

"""
import importlib.util
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("textos", Path(__file__).with_name("textos.py"))
TX = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(TX)

REPO = "https://github.com/Falkzera/Falkzera/blob/main"


def arquivo(lang):
    return "README.md" if lang == TX.PADRAO else f"README.{lang}.md"


def figura(base, alt, largura):
    return (f'  <picture>\n'
            f'    <source media="(prefers-color-scheme: dark)" srcset="assets/{base}-dark.svg">\n'
            f'    <img src="assets/{base}-light.svg" alt="{alt}" width="{largura}">\n'
            f'  </picture>')


def perfis():
    linhas = []
    for nome, href, rot in TX.PERFIS:
        linhas.append(
            f'  <a href="{href}" title="{rot}"><picture>'
            f'<source media="(prefers-color-scheme: dark)" srcset="assets/btn-{nome}-dark.svg">'
            f'<img src="assets/btn-{nome}-light.svg" alt="{rot}" width="46" height="46">'
            f'</picture></a>')
    return "\n".join(linhas)


def quebrar(texto, largura=92):
    """Quebra em linhas de no maximo `largura`, para o markdown ficar legivel no
    diff. Markdown junta linha simples num paragrafo so, entao isso nao muda o
    que o leitor ve."""
    linhas, atual = [], ""
    for palavra in texto.split():
        if atual and len(atual) + 1 + len(palavra) > largura:
            linhas.append(atual); atual = palavra
        else:
            atual = f"{atual} {palavra}".strip()
    if atual:
        linhas.append(atual)
    return "\n".join(linhas)


def montar(lang):
    return "\n".join([
        '<div align="center">',
        figura("banner", TX.ALT_BANNER[lang], 900),
        "</div>",
        "",
        quebrar(TX.INTRO[lang]),
        "",
        quebrar(TX.PRIVADO[lang]),
        "",
        '<div align="center">',
        figura("stack", TX.ALT_STACK[lang], 900),
        "</div>",
        "",
        quebrar(TX.PESQUISA[lang]),
        "",
        '<div align="center">',
        perfis(),
        "</div>",
        "",
    ])


if __name__ == "__main__":
    conteudo = montar(TX.PADRAO)
    assert "—" not in conteudo and "–" not in conteudo, "travessao no README"
    (RAIZ / "README.md").write_text(conteudo, encoding="utf-8")
    print(f"README.md  {len(conteudo.split())} palavras  idioma {TX.PADRAO}")
