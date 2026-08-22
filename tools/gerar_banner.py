#!/usr/bin/env python3
"""Gera o banner animado do README do perfil, nos temas claro e escuro.

    python3 tools/gerar_banner.py

Sai `assets/banner-dark.svg` e `assets/banner-light.svg`, consumidos pelo README
via `<picture>` com `prefers-color-scheme`.

Tres telas de terminal. Apresentacao, arvore de habilidades e listagem dos
projetos. O fecho nao e uma tela propria: e o rodape da ultima, onde o
`open https://lucasfalcao.dev.br` e digitado e fica piscando.

COMO A TELA VIRA. Nao existe `clear`. Cada tela termina com o comando da tela
SEGUINTE sendo digitado no rodape, e so entao a tela troca, ja com aquele comando
no topo e a saida nascendo embaixo. E como um terminal se comporta quando rola.

A ARVORE E DESENHADA, NAO ESCRITA. Os ramos sao `<path>` com traco, e nao os
caracteres de quadro `├──` e `└──`. Caractere de quadro depende de a fonte do
visitante ter o glifo no avanco certo, e quando nao tem, aparece emenda entre um
pedaco e outro do ramo. Traco vetorial fecha sempre.

POR QUE NAO EXISTE `textLength`. Ele quebrou feio. O SVG colapsa espaco repetido,
entao `len(texto)` conta caractere que nao e desenhado, o comprimento forcado
fica maior que o natural e o navegador estica a linha com espacamento entre
letras.

COMO O CORTE DA DIGITACAO NAO DECEPA MAIS. Duas travas, e as duas sao
necessarias. A regua anda com avanco de 0.63em, um pouco MAIOR que o 0.6em real
da monoespacada, entao ela vai sempre um fio na frente do glifo em vez de atras.
E o ultimo passo pula direto para a largura inteira do quadro, entao o estado
final revela tudo por construcao, independentemente da fonte que o visitante
tenha. Estimar largura de fonte com precisao e uma briga que nao se ganha, o
jeito e nao depender da estimativa no fim.

A SEGUNDA COLUNA E CALCULADA POR TELA. Cada tela alinha a coluna de comentario
pelo seu proprio nome mais longo. Fixar um x unico obrigava a caber o pior caso
de todas as telas, e sobrava vao nas outras.

Por que SVG proprio e nao servico de terceiro. O banner precisa continuar de pe
sem depender de site externo, e falar a mesma lingua do lucasfalcao.dev.br. As
cores sao os tokens de `globals.css`, copiados sem adaptacao.

Por que SMIL e nao CSS. O SVG entra no README como `<img>`, e nesse contexto o
navegador renderiza documento isolado, sem script e sem recurso externo.
"""
import importlib.util
from pathlib import Path
from xml.sax.saxutils import escape

_spec = importlib.util.spec_from_file_location("textos", Path(__file__).with_name("textos.py"))
TX = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(TX)

TEMAS = {
    "dark": dict(surface="#10131f", line="#1f2436", fog="#838ca6", ramo="#3a4straight",
                 body="#aab3c9", title="#f2f5fc", glow="#4d7cff", azure="#8fb0ff"),
    "light": dict(surface="#ffffff", line="#d7e0f2", fog="#5b6a8c", ramo="#b9c6e0",
                  body="#35425e", title="#0b1526", glow="#2f5fe0", azure="#2563eb"),
}
TEMAS["dark"]["ramo"] = "#39415c"

W = 900
X = 30
BARRA = 36
TOPO = 34
MONO = "ui-monospace,SFMono-Regular,SF Mono,Menlo,Consolas,Liberation Mono,monospace"
AVANCO = 0.6      # avanco real da monoespacada, usado para POSICIONAR
REGUA = 0.63      # avanco da regua de digitacao, de proposito maior que o real
VAO2 = 26         # respiro entre o nome mais longo e a segunda coluna
RECUO = 34        # indentacao do filho da arvore
CMD, SAI = 0.058, 0.013


def linha(txt, nota=None, cor="body", fonte=14.5, alt=23, seg=None, ramo=False, ultimo=False):
    return dict(txt=txt, nota=nota, cor=cor, fonte=fonte, alt=alt, ramo=ramo, ultimo=ultimo,
                seg=SAI if seg is None else seg)

def ramo(txt, nota, ultimo=False):
    return linha(txt, nota, cor="azure", ramo=True, ultimo=ultimo)

def branco(alt=13):
    return linha("", alt=alt, seg=0.0)


def telas_de(lang):
    """Monta as tres telas no idioma pedido.

    Nome de pasta, nome de projeto e a saida do `tree` NAO passam pelo dicionario.
    `build/`, `governanca-mais/` e "5 directories" sao iguais nos quatro idiomas,
    porque diretorio nao se traduz e `tree` imprime em ingles em toda maquina."""
    return [
        dict(cmd="whoami", segura=2.2, saida=[
            branco(10),
            linha("Lucas Falcão", cor="title", fonte=31, alt=44, seg=0.085),
            linha(TX.CARGO[lang], cor="fog", fonte=14, alt=26, seg=0.045),
        ]),
        dict(cmd="cd ~/skills && tree", segura=4.0, saida=[
            branco(12),
            linha("skills/", cor="title"),
            *[ramo(nome, nota, ultimo=(i == len(TX.SKILLS[lang]) - 1))
              for i, (nome, nota) in enumerate(TX.SKILLS[lang])],
            branco(15),
            linha(f"{len(TX.SKILLS[lang])} directories", cor="fog", fonte=12.5, alt=20),
        ]),
        dict(cmd="cd ~/Projects && ls", segura=4.0, saida=[
            branco(12),
            *[linha(nome, nota, cor="azure") for nome, nota in TX.PROJETOS[lang]],
        ]),
    ]


FINAL = "open https://lucasfalcao.dev.br"


def montar(lang):
    TELAS = telas_de(lang)
    t, telas, alturas = 0.0, [], []
    for i, tela in enumerate(TELAS):
        # a segunda coluna desta tela alinha pelo nome mais longo dela
        com_nota = [l for l in tela["saida"] if l["nota"]]
        col2 = 0
        for l in com_nota:
            base = X + (RECUO if l["ramo"] else 0) + len(l["txt"]) * l["fonte"] * AVANCO
            col2 = max(col2, base + VAO2)

        ini, y, itens = t, BARRA + TOPO, []
        seg = CMD if i == 0 else 0.0
        itens.append(dict(tipo="cmd", txt=tela["cmd"], y=y, t0=t, t1=t + seg * len(tela["cmd"]),
                          fonte=15, cor="body", cols=len(tela["cmd"]) + 2, ramo=False,
                          nota=None, col2=col2))
        y += 28
        t = itens[-1]["t1"]
        for ln in tela["saida"]:
            x0 = X + (RECUO if ln["ramo"] else 0)
            fim = x0 + len(ln["txt"]) * ln["fonte"] * AVANCO
            if ln["nota"]:
                fim = max(fim, col2 + len(ln["nota"]) * ln["fonte"] * AVANCO)
            cols = max(1, round((fim - X) / (ln["fonte"] * REGUA)))
            t1 = t + ln["seg"] * cols
            itens.append(dict(ln, tipo="saida", y=y, t0=t, t1=t1, cols=cols, col2=col2))
            y, t = y + ln["alt"], t1
        t += tela["segura"]
        prox = TELAS[i + 1]["cmd"] if i + 1 < len(TELAS) else FINAL
        y += 18
        itens.append(dict(tipo="cmd", txt=prox, y=y, t0=t, t1=t + CMD * len(prox),
                          fonte=15, cor="body", cols=len(prox) + 2, ramo=False,
                          nota=None, col2=col2))
        t = itens[-1]["t1"] + (0.9 if i + 1 < len(TELAS) else 3.2)
        alturas.append(y + 26)
        telas.append(dict(itens=itens, ini=ini, fim=t))
    return telas, t, max(alturas)


def digitar(cid, item, ciclo, H):
    """clipPath que anda um caractere por vez. O ultimo passo pula para a largura
    inteira, que e o que garante revelacao completa sem depender da fonte."""
    n = item["cols"]
    av = item["fonte"] * REGUA
    if item["t1"] - item["t0"] < 0.01:
        vals, chaves = f"{W};{W}", "0;1"
    else:
        larg = [0.0] + [min(av * (c + 1) + 4, W) for c in range(n - 1)] + [float(W)]
        passos = [item["t0"] + (item["t1"] - item["t0"]) * (c + 1) / n for c in range(n)]
        chaves = ["0"] + [str(round(max(0.0, min(1.0, s / ciclo)), 5)) for s in passos]
        vals = ";".join(f"{v:.1f}" for v in larg)
        chaves = ";".join(chaves)
    return (f'<clipPath id="{cid}"><rect x="{X}" y="0" height="{H}" width="0">'
            f'<animate attributeName="width" dur="{ciclo}s" repeatCount="indefinite"'
            f' calcMode="discrete" values="{vals}" keyTimes="{chaves}"/></rect></clipPath>')


def gerar(tema, telas, ciclo, H, lang):
    c, defs, corpo = TEMAS[tema], [], []
    k = lambda s: round(max(0.0, min(1.0, s / ciclo)), 5)
    n = 0
    for tela in telas:
        a0, a1 = k(tela["ini"]), k(tela["fim"])
        grupo, y_ramo_ant = [], None
        for item in tela["itens"]:
            if not item["txt"] and not item.get("nota"):
                continue
            n += 1
            cid = f"d{n}"
            defs.append(digitar(cid, item, ciclo, H))
            av = item["fonte"] * AVANCO
            x0 = X + (RECUO if item.get("ramo") else 0)
            peca = ""
            if item.get("ramo"):
                # tronco vindo do irmao anterior (ou da raiz) ate a altura desta
                # linha, e o gancho horizontal ate o nome
                cy = item["y"] - item["fonte"] * 0.33
                topo = y_ramo_ant if y_ramo_ant is not None else item["y"] - item["alt"] + 2
                tx = X + 8
                peca += (f'<path d="M{tx} {topo:.1f} V{cy:.1f} H{x0 - 8}" fill="none"'
                         f' stroke="{c["ramo"]}" stroke-width="1.4" stroke-linecap="round"'
                         f' stroke-linejoin="round"/>')
                y_ramo_ant = cy
            if item["tipo"] == "cmd":
                peca += (f'<text x="{X}" y="{item["y"]}" font-size="{item["fonte"]}"'
                         f' fill="{c["glow"]}" xml:space="preserve">$ '
                         f'<tspan fill="{c["body"]}">{escape(item["txt"])}</tspan></text>')
                cx = X + av * (len(item["txt"]) + 2) + 3
            else:
                peca += (f'<text x="{x0:.1f}" y="{item["y"]}" font-size="{item["fonte"]}"'
                         f' fill="{c[item["cor"]]}" xml:space="preserve">{escape(item["txt"])}</text>')
                if item.get("nota"):
                    peca += (f'<text x="{item["col2"]:.1f}" y="{item["y"]}"'
                             f' font-size="{item["fonte"]}" fill="{c["fog"]}"'
                             f' xml:space="preserve">{escape(item["nota"])}</text>')
                cx = x0 + av * len(item["txt"]) + 3
            grupo.append(f'<g clip-path="url(#{cid})">{peca}</g>')
            if item is tela["itens"][-1]:
                passos, vals, s, on = [], [], item["t1"], True
                while s < tela["fim"] - 0.05:
                    passos.append(k(s)); vals.append("1" if on else "0")
                    s, on = s + 0.46, not on
                if passos:
                    grupo.append(
                        f'<rect x="{cx:.1f}" y="{item["y"] - item["fonte"] * 0.82:.1f}"'
                        f' width="{av * 0.9:.1f}" height="{item["fonte"] * 1.08:.1f}"'
                        f' fill="{c["glow"]}" opacity="0"><animate attributeName="opacity"'
                        f' dur="{ciclo}s" repeatCount="indefinite" calcMode="discrete"'
                        f' values="0;{";".join(vals)};0"'
                        f' keyTimes="0;{";".join(str(x) for x in passos)};{a1}"/></rect>')
        corpo.append(
            f'<g opacity="0">{"".join(grupo)}'
            f'<animate attributeName="opacity" dur="{ciclo}s" repeatCount="indefinite"'
            f' calcMode="discrete" values="0;1;0" keyTimes="0;{a0};{a1}"/></g>')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{escape(TX.ALT_BANNER[lang])}">
<defs>
{chr(10).join(defs)}
</defs>
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="12" fill="{c['surface']}" stroke="{c['line']}" stroke-width="1.5"/>
<line x1="1" y1="{BARRA}" x2="{W-1}" y2="{BARRA}" stroke="{c['line']}" stroke-width="1.5"/>
<circle cx="27" cy="18.5" r="5" fill="{c['line']}"/>
<circle cx="47" cy="18.5" r="5" fill="{c['line']}"/>
<circle cx="67" cy="18.5" r="5" fill="{c['line']}"/>
<text x="{W-28}" y="23" text-anchor="end" font-family="{MONO}" font-size="12.5" fill="{c['fog']}">falkzera ~ github</text>
<g font-family="{MONO}">
{chr(10).join(corpo)}
</g>
</svg>
'''


if __name__ == "__main__":
    destino = Path(__file__).resolve().parent.parent / "assets"
    destino.mkdir(exist_ok=True)
    lang = TX.PADRAO
    telas, ciclo, H = montar(lang)
    for tema in TEMAS:
        alvo = destino / f"banner-{tema}.svg"
        alvo.write_text(gerar(tema, telas, ciclo, H, lang), encoding="utf-8")
        print(f"{alvo.name}  {alvo.stat().st_size // 1024} KB")
    print(f"ciclo {ciclo:.1f}s  altura {H}px  {len(telas)} telas  idioma {lang}")
