#!/usr/bin/env python3
"""Renderiza UM QUADRO ESTATICO por tela do banner, para conferir alinhamento.

    python3 tools/quadros.py [idioma]

Sai `assets/quadro-1.svg`, `quadro-2.svg`, ... com aquela tela inteiramente
digitada e nenhuma animacao. E como se revisa layout sem depender de acertar o
instante certo da animacao, que com SMIL nao da para controlar de fora.
"""
import importlib.util
from pathlib import Path
from xml.sax.saxutils import escape

RAIZ = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("gb", RAIZ / "tools" / "gerar_banner.py")
gb = importlib.util.module_from_spec(spec); spec.loader.exec_module(gb)


def quadro(tema, tela, H):
    c, partes = gb.TEMAS[tema], []
    quadro.ant = None
    for item in tela["itens"]:
        if not item["txt"] and not item.get("nota"):
            continue
        x0 = gb.X + (gb.RECUO if item.get("ramo") else 0)
        if item.get("ramo"):
            cy = item["y"] - item["fonte"] * 0.33
            topo = quadro.ant if quadro.ant is not None else item["y"] - item["alt"] + 2
            partes.append(f'<path d="M{gb.X + 8} {topo:.1f} V{cy:.1f} H{x0 - 8}" fill="none"'
                          f' stroke="{c["ramo"]}" stroke-width="1.4" stroke-linecap="round"'
                          f' stroke-linejoin="round"/>')
            quadro.ant = cy
        if item["tipo"] == "cmd":
            partes.append(f'<text x="{gb.X}" y="{item["y"]}" font-size="{item["fonte"]}"'
                          f' fill="{c["glow"]}" xml:space="preserve">$ '
                          f'<tspan fill="{c["body"]}">{escape(item["txt"])}</tspan></text>')
        else:
            partes.append(f'<text x="{x0:.1f}" y="{item["y"]}" font-size="{item["fonte"]}"'
                          f' fill="{c[item["cor"]]}" xml:space="preserve">{escape(item["txt"])}</text>')
            if item.get("nota"):
                partes.append(f'<text x="{item["col2"]:.1f}" y="{item["y"]}" font-size="{item["fonte"]}"'
                              f' fill="{c["fog"]}" xml:space="preserve">{escape(item["nota"])}</text>')
    W = gb.W
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
            f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="12" fill="{c["surface"]}"'
            f' stroke="{c["line"]}" stroke-width="1.5"/>'
            f'<line x1="1" y1="{gb.BARRA}" x2="{W-1}" y2="{gb.BARRA}" stroke="{c["line"]}" stroke-width="1.5"/>'
            f'<circle cx="27" cy="18.5" r="5" fill="{c["line"]}"/>'
            f'<circle cx="47" cy="18.5" r="5" fill="{c["line"]}"/>'
            f'<circle cx="67" cy="18.5" r="5" fill="{c["line"]}"/>'
            f'<text x="{W-28}" y="23" text-anchor="end" font-family="{gb.MONO}" font-size="12.5"'
            f' fill="{c["fog"]}">falkzera ~ github</text>'
            f'<g font-family="{gb.MONO}">{"".join(partes)}</g></svg>\n')


if __name__ == "__main__":
    import sys
    lang = sys.argv[1] if len(sys.argv) > 1 else "en"
    telas, ciclo, H = gb.montar(lang)
    for i, tela in enumerate(telas, 1):
        alvo = RAIZ / "assets" / f"quadro-{lang}-{i}.svg"
        alvo.write_text(quadro("dark", tela, H), encoding="utf-8")
        print(f"{alvo.name}  tela {i}")
