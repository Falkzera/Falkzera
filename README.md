## Lucas Falcão

**Engenheiro de Software · Economista pela UFAL**
Economia para entender o problema, engenharia para construir a resposta.

Construo software para o setor público em Alagoas. O arco se repetiu três vezes. Uma
planilha que não aguentava mais, um protótipo, e um sistema institucional no lugar dela.

---

> ### Por que a estante aqui está quase vazia
>
> O gráfico de contribuições logo abaixo é real, **mais de 3.600 no último ano**. Só que
> quase todas moram em repositório privado, porque software de órgão público tem código
> que não é meu para abrir.
>
> O que dá para mostrar está em **[lucasfalcao.dev.br](https://lucasfalcao.dev.br)**, com
> o que cada sistema fez, o que mudou depois dele, e a declaração institucional assinada
> que atesta cada afirmação.

---

### Os sistemas

#### Governança+ · Sec. de Governança Corporativa de Alagoas · desde 2025

Plataforma corporativa usada pelas secretarias do Estado. Substituiu a planilha em que
cerca de oito monitores digitavam à mão o que os órgãos mandavam por foto e PDF. Hoje
**mais de 200 servidores, em 46 órgãos**, alimentam a base direto, com regra de negócio
aplicada na entrada e fila de validação humana antes de o dado virar relatório.

Sou **um dos responsáveis técnicos**, porque é projeto de equipe e não sou o autor dele.
Assino a versão inicial, a criação do repositório e da estrutura da versão atual, o
módulo de coleta e validação de entregas, a intranet com chat em tempo real, o mapa
georreferenciado de obras e o agente de LLM que escreve consulta de leitura a partir de
pergunta em português, validada antes de tocar o banco.

`TypeScript` · `React` · `Node.js` · `PostgreSQL` · `Drizzle ORM` · `WebSocket` · `Docker` · `Kubernetes` · `CI/CD`

#### JÁ! Em Dados · SEPLAG/AL · 2025

Acabou com o relatório executivo feito à mão, um por vez, nas onze Centrais JÁ!. ETL
incremental e idempotente sobre 1,1 milhão de registros. A origem territorial dos cidadãos
saiu por geocodificação offline contra a malha de faces de logradouro do IBGE, e não por
API de terceiro, o que levou o custo por consulta a **R$ 0** em centenas de milhares de
endereços. **Três meses da concepção ao handover documentado**, como responsável técnico.

`Python` · `pandas` · `Parquet` · `Streamlit`

#### SIGOF · SEPLAG/AL · 2024 a 2025

Tirou o controle do crédito suplementar do Estado de uma planilha sem trilha de auditoria.
O relatório institucional era redigido à mão todo mês e passou a sair por código, **de
dias para minutos**. O limite legal é calculado em tempo real, com o teto derivado do
texto da lei, e cada alteração carimba autor e horário.

`Python` · `pandas` · `Parquet` · `Streamlit` · `React` · `TypeScript`

---

### Pesquisa

**"Taxa de cesárea em hospitais públicos e privados no Brasil: uma análise da demanda
induzida pela oferta, 2014-2022"**, TCC em Ciências Econômicas, UFAL.

Microdados do SINASC pareados com o CNES, por três métodos encadeados. Aprendizado de
máquina (XGBoost, LightGBM), escore de propensão com ponderação pelo inverso da
probabilidade, e diferenças em diferenças com os estimadores de Sun e Abraham e de
Callaway e Sant'Anna.

[Lattes](http://lattes.cnpq.br/7114371121090791) · [ORCID](https://orcid.org/0009-0007-2130-5697)

---

### Aberto aqui

**[falcao-skills-open](https://github.com/Falkzera/falcao-skills-open)**, Agent Skills open
source. A `lgpd-compliance` audita um app inteiro contra LGPD, ANPD, CDC e Marco Civil e
devolve os artefatos prontos, da política de privacidade ao ROPA, ao RIPD e ao runbook de
incidente. MIT.

**[hitman-mac-modding](https://github.com/Falkzera/hitman-mac-modding)**, modding nativo do
HITMAN World of Assassination em Rust, no Apple Silicon.

---

[**lucasfalcao.dev.br**](https://lucasfalcao.dev.br) · [LinkedIn](https://linkedin.com/in/falkzera) · lucasmatheusfalcao@hotmail.com
