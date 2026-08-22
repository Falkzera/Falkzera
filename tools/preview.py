#!/usr/bin/env python3
"""Monta preview.html com o README nos dois temas.

    python3 tools/preview.py && python3 -m http.server 8899

Nao vai para o GitHub, e ferramenta de revisao.

TRES ARMADILHAS que ja morderam aqui, e por isso o codigo e do jeito que e:

1. INLINAR o SVG no HTML quebra. O SMIL do carrossel nao dispara e dois paineis
   emitem clipPath com id igual, um sobrescrevendo o outro. O GitHub referencia
   por `<img>`, entao inlinar tambem mentia sobre o resultado. Aqui vai `<img>`.
2. Nao basta ver se o bloco comeca com `<div align`. Existem quatro deles por
   arquivo, e casar pelo comeco fazia o carrossel renderizar duas vezes. A
   deteccao olha o conteudo.
3. O `<picture>` escolhe pelo `prefers-color-scheme` DO NAVEGADOR, que nao sabe
   nada dos paineis falsos desta pagina. Deixar intacto mostrava botao escuro
   sobre fundo branco. A variante certa e forcada na mao.
"""
import html
import importlib.util
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("textos", Path(__file__).with_name("textos.py"))
TX = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(TX)


def inline(s):
    s = re.sub(r"`([^`]+)`", lambda m: "<code>" + html.escape(m.group(1)) + "</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)


def figuras(b, tema):
    """Reescreve um bloco de figura para a variante do tema deste painel."""
    if "banner-" in b:
        return f'<div class="banner"><img src="assets/banner-{tema}.svg" alt=""></div>'
    if "stack-" in b:
        return f'<div class="stack"><img src="assets/stack-{tema}.svg" alt=""></div>'
    if "btn-" in b:
        botoes = re.findall(r'<a href="([^"]+)"[^>]*>.*?btn-([a-z]+)-', b, re.S)
        return '<div class="botoes">' + "".join(
            f'<a href="{h}"><img src="assets/btn-{n}-{tema}.svg" alt=""></a>'
            for h, n in botoes) + "</div>"
    return ""


def render(md, tema):
    out = []
    for b in [x.strip() for x in md.split("\n\n") if x.strip()]:
        if any(k in b for k in ("banner-", "stack-", "btn-")):
            out.append(figuras(b, tema))
        elif b.startswith("<div") or b.startswith("</div"):
            continue
        else:
            out.append("<p>" + inline(b) + "</p>")
    return "\n".join(out)


CSS = """*{box-sizing:border-box}body{margin:0;background:#0d1117;font-family:ui-sans-serif,-apple-system,Segoe UI,sans-serif}
.faixa{padding:10px 20px 0}.faixa h2{max-width:920px;margin:26px auto 0;color:#f2f5fc;font:600 15px/1 ui-monospace,monospace;letter-spacing:.1em;text-transform:uppercase}
.painel{padding:14px 20px 40px}.painel.dark{background:#0d1117}.painel.light{background:#fff}
.chip{max-width:920px;margin:0 auto 12px;font:600 11px/1 ui-monospace,monospace;letter-spacing:.14em;text-transform:uppercase;opacity:.6}
.dark .chip{color:#8fb0ff}.light .chip{color:#2f5fe0}
.readme{max-width:920px;margin:0 auto;border-radius:10px;padding:26px 32px 34px;font-size:15.5px;line-height:1.65}
.dark .readme{background:#0d1117;border:1px solid #30363d;color:#c9d1d9}
.light .readme{background:#fff;border:1px solid #d0d7de;color:#1f2328}
.banner{margin:-6px 0 18px}.banner img,.stack img{width:100%;height:auto;display:block}
.stack{margin:24px 0 10px}p{margin:14px 0}
.botoes{display:flex;gap:10px;justify-content:center;margin:26px 0 6px}
.botoes img{width:46px;height:46px;display:block}
code{font:12.5px/1 ui-monospace,SFMono-Regular,Menlo,monospace;padding:.2em .45em;border-radius:6px}
.dark code{background:#6e768166}.light code{background:#afb8c133}
a{text-decoration:none}a:hover{text-decoration:underline}.dark a{color:#4493f8}.light a{color:#0969da}
strong{font-weight:600}.dark strong{color:#e6edf3}.light strong{color:#1f2328}"""

if __name__ == "__main__":
    md = (RAIZ / "README.md").read_text(encoding="utf-8")
    partes = []
    for tema in ("dark", "light"):
        partes.append(
            f'<section class="painel {tema}"><div class="chip">'
            f'modo {"escuro" if tema == "dark" else "claro"}</div>'
            f'<div class="readme">{render(md, tema)}</div></section>')
    quadros = sorted((RAIZ / "assets").glob("quadro-*.svg"))
    if quadros:
        partes.append('<section class="painel dark"><div class="chip">quadros estaticos do'
                      ' terminal, com todo corte aberto</div><div class="readme">'
                      + "".join(f'<div class="banner"><img src="assets/{q.name}" alt=""></div>'
                                for q in quadros) + "</div></section>")
    (RAIZ / "preview.html").write_text(
        '<!doctype html><meta charset="utf-8"><title>Preview do README</title>'
        f"<style>{CSS}</style>" + "".join(partes), encoding="utf-8")
    print("preview.html regerado")
