#!/usr/bin/env python3
"""Fonte de verdade do texto do README.

⚠ SO O INGLES E EMITIDO HOJE, e isso e decisao, nao esquecimento. As traducoes
ficam aqui porque ja estao feitas e conferidas, e porque separar texto de layout
vale mesmo com um idioma so.

POR QUE O SELETOR DE IDIOMA FOI DESCARTADO (21/08/2026). Nao existe jeito de o
README trocar de idioma sozinho. Nao roda JavaScript, o GitHub remove script; nao
existe media query de idioma, o `<picture>` acerta o tema porque
`prefers-color-scheme` e media feature de verdade e nao ha equivalente para
lingua; e detectar pela imagem tambem falha, porque toda imagem passa pelo proxy
camo, que faz a requisicao no lugar do visitante E CACHEIA a resposta para todos.

Sobravam duas saidas, e as duas foram recusadas:

1. Um arquivo por idioma, com bandeira clicavel. Funciona, mas a pagina do perfil
   serve SEMPRE o `README.md`, entao clicar na bandeira JOGA O VISITANTE FORA DO
   PERFIL, para a tela de arquivo do repo. Ele perde a barra lateral, os repos
   fixados e o grafico de contribuicoes, que e justamente onde esta a prova.
2. Os outros idiomas em `<details>` no mesmo arquivo, expandindo no lugar. Nao sai
   do perfil, mas engorda a pagina e o banner traduzido nao vem junto.

Decisao do Falcao: README so em ingles. Se um dia voltar o assunto, o caminho
menos ruim e o `<details>`, e nao o arquivo separado.

Mesma lei de i18n do lucas-falcao-site, e vale nos quatro idiomas:

TERMO TECNICO CONSAGRADO NAO SE TRADUZ. `full stack`, `ETL`, `deploy`, `schema`,
`handover`, `commit`, `read only`, `geocoding`, `data scientist` e `software
engineer` ficam como estao. Escrever "pilha completa" ou "implantacao" soa amador
e ainda quebra a busca do recrutador, que procura o termo em ingles.

NOME PROPRIO, SIGLA, NUMERO E NOME DE PASTA NAO ENTRAM AQUI. `governanca-mais`,
`SIGOF`, `LGPD`, `R$ 0`, `1.1M` e os nomes dos diretorios do terminal sao iguais
nos quatro idiomas, e por isso vivem no gerador e nao no dicionario.

A SAIDA DO `tree` FICA EM INGLES. "5 directories" e o que o comando imprime de
verdade em qualquer maquina; traduzir seria mentir sobre a ferramenta.
"""

IDIOMAS = ["en", "pt", "es", "de"]
PADRAO = "en"

NOMES = {"en": "English", "pt": "Português", "es": "Español", "de": "Deutsch"}

# ─── terminal ──────────────────────────────────────────────────────────────────

CARGO = {
    "en": "Economist · Data Scientist · Software Engineer",
    "pt": "Economista · Cientista de Dados · Software Engineer",
    "es": "Economista · Data Scientist · Software Engineer",
    "de": "Ökonom · Data Scientist · Software Engineer",
}

# A tela de skills diz o que ele SABE FAZER, e a de projetos diz o que ele FEZ.
# Sao coisas diferentes de proposito. Enquanto o skills listava ferramenta, ele
# repetia o carrossel logo abaixo e nao acrescentava nada; enquanto listava
# entrega, repetia a tela de projetos. Aqui ficam so as capacidades DIFICEIS,
# afirmadas em uma linha, sem detalhe. Detalhe e o que o site tem.
#
# "data lake" tem lastro: e stack declarada no vinculo do SIGOF em
# `trajetoria.ts` do lucas-falcao-site, e a sub-rota descreve os dez pipelines
# gravando em parquet com deduplicacao.
SKILLS = {
    "en": [("data-engineering/",     "design a data lake and the pipelines that fill it"),
           ("software-engineering/", "ship an application end to end, schema to deploy"),
           ("data-science/",         "measure the causal impact of a public policy"),
           ("ai/",                   "put LLM agents to work inside a real system")],
    "pt": [("data-engineering/",     "desenhar um data lake e os pipelines que o alimentam"),
           ("software-engineering/", "entregar uma aplicação de ponta a ponta, do schema ao deploy"),
           ("data-science/",         "medir o impacto causal de uma política pública"),
           ("ai/",                   "pôr agentes de LLM para trabalhar dentro de um sistema real")],
    "es": [("data-engineering/",     "diseñar un data lake y los pipelines que lo alimentan"),
           ("software-engineering/", "entregar una aplicación de punta a punta, del schema al deploy"),
           ("data-science/",         "medir el impacto causal de una política pública"),
           ("ai/",                   "poner agentes de LLM a trabajar dentro de un sistema real")],
    "de": [("data-engineering/",     "einen Data Lake entwerfen und die Pipelines, die ihn füllen"),
           ("software-engineering/", "eine Anwendung end to end liefern, vom Schema bis zum Deploy"),
           ("data-science/",         "die kausale Wirkung einer öffentlichen Politik messen"),
           ("ai/",                   "LLM-Agenten in einem echten System arbeiten lassen")],
}

# TRES projetos, e cada linha carrega uma forca DIFERENTE. Adocao no
# governanca-mais, desfecho no sigof, rigor de engenharia no peteco. Com as tres
# dizendo "relatorio que era a mao virou automatico" a tela repetiria a si mesma
# e o leitor so guardaria a primeira.
#
# O peteco larga o angulo obvio de propósito. O relatorio do MEC feito a mao ele
# tem, mas isso ja e o que o sigof diz. Privacidade como codigo, com inventario
# LGPD validado no CI a cada PR, e o que o blurb do site descreve e o que quase
# nenhum candidato consegue afirmar.
PROJETOS = {
    "en": [("governanca-mais/", "~8 monitors by hand to 200+ users in 46 agencies"),
           ("sigof/",           "monthly report from days to minutes, audited state"),
           ("peteco/",          "privacy as code, LGPD inventory checked on every PR")],
    "pt": [("governanca-mais/", "~8 monitores à mão para 200+ usuários em 46 órgãos"),
           ("sigof/",           "relatório mensal de dias para minutos, estado auditado"),
           ("peteco/",          "privacidade como código, inventário LGPD conferido a cada PR")],
    "es": [("governanca-mais/", "~8 monitores a mano para 200+ usuarios en 46 organismos"),
           ("sigof/",           "informe mensual de días a minutos, estado auditado"),
           ("peteco/",          "privacidad como código, inventario LGPD revisado en cada PR")],
    "de": [("governanca-mais/", "~8 Erfasser per Hand zu 200+ Nutzern in 46 Behörden"),
           ("sigof/",           "Monatsbericht von Tagen auf Minuten, auditierter Zustand"),
           ("peteco/",          "Privacy as Code, LGPD-Inventar bei jedem PR geprüft")],
}

# ─── README ────────────────────────────────────────────────────────────────────

INTRO = {
    "en": ("Economist, researcher, software engineer and data scientist. I work in the public "
           "sector in Alagoas, Brazil, where I structure the data and then build the systems that "
           "put that structure in front of real users. Data platforms, ETL over millions of rows, "
           "georeferenced maps, and LLM agents that watch a process and raise an alert the moment "
           "a contract rule is broken."),
    "pt": ("Economista, pesquisador, engenheiro de software e cientista de dados. Trabalho no "
           "setor público em Alagoas, no Brasil, onde estruturo o dado e depois construo os "
           "sistemas que põem essa estrutura na frente de quem usa. Plataformas de dados, ETL "
           "sobre milhões de linhas, mapas georreferenciados, e agentes de LLM que vigiam um "
           "processo e avisam no instante em que uma regra de contrato é quebrada."),
    "es": ("Economista, investigador, ingeniero de software y científico de datos. Trabajo en el "
           "sector público en Alagoas, Brasil, donde estructuro el dato y luego construyo los "
           "sistemas que ponen esa estructura frente a quien la usa. Plataformas de datos, ETL "
           "sobre millones de filas, mapas georreferenciados, y agentes de LLM que vigilan un "
           "proceso y avisan en el momento en que se rompe una regla de contrato."),
    "de": ("Ökonom, Forscher, Software Engineer und Data Scientist. Ich arbeite im öffentlichen "
           "Sektor in Alagoas, Brasilien, wo ich die Daten strukturiere und danach die Systeme "
           "baue, die diese Struktur zu echten Nutzern bringen. Datenplattformen, ETL über "
           "Millionen Zeilen, georeferenzierte Karten, und LLM-Agenten, die einen Prozess "
           "überwachen und warnen, sobald eine Vertragsregel gebrochen wird."),
}

PRIVADO = {
    "en": ("Most of that code is institutional and lives in private repositories. For the full "
           "detail, see **[lucasfalcao.dev.br](https://lucasfalcao.dev.br)**."),
    "pt": ("Quase todo esse código é institucional e vive em repositório privado. Para o detalhe "
           "completo, veja **[lucasfalcao.dev.br](https://lucasfalcao.dev.br)**."),
    "es": ("Casi todo ese código es institucional y vive en repositorios privados. Para el detalle "
           "completo, mira **[lucasfalcao.dev.br](https://lucasfalcao.dev.br)**."),
    "de": ("Fast dieser gesamte Code ist institutionell und liegt in privaten Repositories. Alle "
           "Details unter **[lucasfalcao.dev.br](https://lucasfalcao.dev.br)**."),
}

PESQUISA = {
    "en": ("**Research** · I evaluate public policy and measure its causal impact, rather than "
           "reporting the correlation around it."),
    "pt": ("**Pesquisa** · Avalio política pública e meço o impacto causal dela, em vez de "
           "reportar a correlação em volta."),
    "es": ("**Investigación** · Evalúo política pública y mido su impacto causal, en lugar de "
           "reportar la correlación alrededor."),
    "de": ("**Forschung** · Ich evaluiere öffentliche Politik und messe deren kausale Wirkung, "
           "statt die Korrelation daneben zu berichten."),
}

ALT_BANNER = {
    "en": "Terminal session, Lucas Falcao, Economist, Data Scientist and Software Engineer",
    "pt": "Sessão de terminal, Lucas Falcão, Economista, Cientista de Dados e Software Engineer",
    "es": "Sesión de terminal, Lucas Falcão, Economista, Data Scientist y Software Engineer",
    "de": "Terminal-Sitzung, Lucas Falcão, Ökonom, Data Scientist und Software Engineer",
}

ALT_STACK = {
    "en": "Stack by objective: languages, frameworks, databases, data, ai, orchestration",
    "pt": "Stack por objetivo: linguagens, frameworks, bancos, dados, ia, orquestração",
    "es": "Stack por objetivo: lenguajes, frameworks, bases, datos, ia, orquestación",
    "de": "Stack nach Zweck: Sprachen, Frameworks, Datenbanken, Daten, KI, Orchestrierung",
}

PERFIS = [
    ("site",      "https://lucasfalcao.dev.br",                  "lucasfalcao.dev.br"),
    ("linkedin",  "https://linkedin.com/in/falkzera",            "LinkedIn"),
    ("instagram", "https://www.instagram.com/falkzera/",         "Instagram"),
    ("lattes",    "http://lattes.cnpq.br/7114371121090791",      "Lattes"),
    ("orcid",     "https://orcid.org/0009-0007-2130-5697",       "ORCID"),
    ("email",     "mailto:lucasmatheusfalcao@hotmail.com",       "e-mail"),
]
