# Planejamento do trabalho do Eduardo (Ritchie)

**Título provisório.** Índice de Precipitação Padronizada no estado do Paraná associado aos eventos de El Niño-Oscilação Sul

**Orientador.** Prof. Dr. Fabrício Correia de Oliveira (UTFPR, Campus Santa Helena)
**Fase.** TCC2. O projeto (TCC1) já foi escrito; este roteiro começa nas análises e termina na escrita dos Resultados e Discussão.
**Produtos.** TCC2 (Google Docs), resumo no SICITE e, se os resultados permitirem, um artigo (alvo inicial *Agrometeoros* ou *Revista Brasileira de Climatologia*).

| Onde fica o quê | Link |
|---|---|
| Projeto do TCC1 (texto aprovado) | `Projeto_TCC1_RITCHIE.docx` |
| TCC2 (texto, escrito ao longo das etapas) | [Google Docs, TCC_ritchie_utfpr](https://docs.google.com/document/d/1P9D4LkLHdXI7kn__TAf4QvMt8qKqxE0d4CG8fD0DBH8/edit?usp=sharing) |
| Código, dados e notebooks | `github.com/fcoliveira-utfpr/spi_oni_pr` |
| Caderno de aprendizagem (antes dos notebooks do TCC) | [00_aprendizagem no Colab](https://colab.research.google.com/github/fcoliveira-utfpr/spi_oni_pr/blob/main/notebooks/00_aprendizagem.ipynb) |
| Resultados das análises | Seu Google Drive, pasta `spi_oni_pr/resultados` (criada pelos notebooks) |

---

## Sumário

- [Como ler este documento](#como-ler-este-documento)
- [A pesquisa em uma página](#a-pesquisa-em-uma-página)
- [Os dados](#os-dados)
- [Como o trabalho roda no Colab](#como-o-trabalho-roda-no-colab)
- [Caderno de aprendizagem](#caderno-de-aprendizagem)
- [Etapa 1. Colab e Python básico](#etapa-1-colab-e-python-básico)
- [Etapa 2. Conhecendo os dados de chuva](#etapa-2-conhecendo-os-dados-de-chuva)
- [Etapa 3. Homogeneidade e tendência](#etapa-3-homogeneidade-e-tendência)
- [Etapa 4. Ajuste das distribuições de probabilidade](#etapa-4-ajuste-das-distribuições-de-probabilidade)
- [Etapa 5. Cálculo do SPI-3 e do SPI-12](#etapa-5-cálculo-do-spi-3-e-do-spi-12)
- [Etapa 6. Classificação do ENOS pelo ONI](#etapa-6-classificação-do-enos-pelo-oni)
- [Etapa 7. Relação entre SPI e ENOS](#etapa-7-relação-entre-spi-e-enos)
- [Etapa 8. Figuras e tabelas finais](#etapa-8-figuras-e-tabelas-finais)
- [Etapa 9. Escrita do TCC2](#etapa-9-escrita-do-tcc2)
- [Pontos de decisão, riscos e referências](#pontos-de-decisão-com-o-orientador)

---

## Como ler este documento

Este é o roteiro do seu TCC2, da primeira análise ao texto final. Cada etapa tem:

1. **Objetivo**: o que a etapa resolve e por que ela existe;
2. **Botão "Open in Colab"**: abre o notebook da etapa no navegador, pronto para rodar;
3. **O que o notebook faz**: as seções do notebook, na ordem;
4. **Trecho explicado**: um bloco de código importante, para você entender antes de rodar;
5. **O que observar**: o que conferir nos resultados;
6. **Entregar**: o critério para passar à etapa seguinte;
7. **O que escrever**: o trecho do TCC2 que nasce daquela etapa.

Você não precisa saber programar para começar. Os notebooks são escritos **da forma mais simples possível**, sem
truques: cada bloco de código tem um texto antes, explicando o que ele faz, e comentários em cada linha. As contas
estatísticas mais longas (ajuste das distribuições, SPI, bootstrap) estão em funções na pasta `src/`, também
comentadas. Seu trabalho é rodar, entender cada passo, interpretar os resultados e escrever.

---

## A pesquisa em uma página

### Pergunta

O El Niño deixa o Paraná mais chuvoso e a La Niña o deixa mais seco? Em que época do ano, com quanto atraso e com que
intensidade? Essa resposta é igual em todo o estado ou muda entre as regiões (Oeste, Norte, Sul, Litoral...)?

### O que é cada índice

```
SPI-3   chuva acumulada em 3 meses, transformada em "desvios padrão" em relação ao normal daquele trimestre
        SPI-3 de novembro = chuva de setembro + outubro + novembro (a primavera)
        → seca agrícola: umidade do solo nas fases críticas das lavouras
SPI-12  chuva acumulada em 12 meses
        → seca hidrológica: rios, reservatórios, lençol freático
ONI     anomalia da temperatura do mar na região Niño 3.4 (média de 3 meses)
        ONI ≥ +0,5 °C por 5 trimestres seguidos → El Niño;  ONI ≤ −0,5 °C → La Niña
```

Por que SPI-3 e SPI-12: o SPI-3 casa com as estações do ano (verão DJF, outono MAM, inverno JJA, primavera SON) e com
os trimestres do ONI, o que permite a análise **por estação do ano**; o SPI-12 mostra o efeito acumulado de um evento
inteiro de ENOS.

### Hipótese

As fases extremas do ENOS modulam a chuva no Paraná de forma **assimétrica e sazonal**: o El Niño aumenta a frequência
de SPI fortemente positivo (excesso), sobretudo na primavera e no Sul e Oeste do estado; a La Niña aumenta a frequência
de SPI fortemente negativo (seca agrícola e hidrológica).

### Como a relação SPI × ENOS é mostrada

A relação é mostrada de duas formas, que se completam:

| Visual (figuras) | Numérica (testes e índices) |
|---|---|
| Série do SPI com faixas coloridas nas fases do ENOS | Correlação ONI × SPI por estação do ano (Pearson e Spearman), com significância por bootstrap em blocos |
| Dispersão ONI × SPI, pontos coloridos pela fase | Correlação defasada (0 a 12 meses): em que defasagem o sinal é mais forte |
| Mapa de calor: correlação por mês × defasagem | Tabela de contingência fase × classe do SPI, qui-quadrado, **probabilidade condicional** e risco relativo |
| Mapas do Paraná com a correlação e a probabilidade de seca em La Niña | Kruskal-Wallis + Dunn: o SPI difere entre El Niño, Neutro e La Niña? E entre as intensidades? |

A **probabilidade condicional** é a análise central: "em anos de La Niña, a chance de uma primavera seca
(SPI-3 ≤ −1) é X%, contra Y% em um ano qualquer". É o número que interessa ao ZARC, ao seguro agrícola e ao produtor.

### Objetivos

**Geral.** Avaliar a variabilidade da precipitação no Paraná por meio do SPI nas escalas trimestral e anual e sua
associação com as fases do ENOS, caracterizadas pelo ONI.

**Específicos.**

- Selecionar a função de distribuição de probabilidade (Gama, Gumbel, Log-Normal ou Exponencial) de melhor ajuste às
  chuvas acumuladas em 3 e 12 meses;
- Calcular o SPI-3 e o SPI-12 e caracterizar os eventos de seca e de excesso hídrico (frequência, duração e severidade);
- Classificar as fases e a intensidade dos eventos ENOS de 1981 a 2020 pelo ONI;
- Quantificar a associação entre o ONI e o SPI por estação do ano e por defasagem;
- Estimar a probabilidade de seca e de excesso hídrico condicionada à fase do ENOS e mapeá-la no Paraná, com destaque
  para a região Oeste.

---

## Os dados

Todos os dados já estão na pasta `dados/` do repositório. **Você não precisa baixar nada**: os notebooks leem os
arquivos direto do GitHub.

| Arquivo | O que tem |
|---|---|
| `estacoes_pr.csv` | Uma linha por pluviômetro: código, município, mesorregião, latitude, longitude, altitude e % de dias preenchidos |
| `chuva_mensal_pr.csv` | Chuva mensal (mm) de cada estação, 01/1981 a 07/2020, e quantos dias do mês foram preenchidos |
| `chuva_diaria_destaque.csv` | Chuva diária das estações em destaque do Oeste (usada para aprender) |
| `oni.csv` | ONI do NOAA/CPC, 1950 em diante: trimestre, ano e anomalia (°C) |
| `pr_mesorregioes.geojson`, `pr_municipios.geojson` | Limites do IBGE, para os mapas |

**De onde vêm.** Pluviômetros da ANA, do INMET e das redes estaduais usados por Xavier et al. (2022), com as falhas
diárias preenchidas pela grade BR-DWGD dos mesmos autores. A série de cada estação foi recortada de 01/01/1981 a
31/07/2020. Só ficaram as estações com a série completa nessa janela e com no máximo 10% dos dias preenchidos:
**370 estações**, de 27 a 50 por mesorregião (44 no Oeste). A exceção é a estação de Foz do Iguaçu (2554002), que
termina em 12/2019 e foi mantida por ser uma das estações em destaque.
O ONI vem do Climate Prediction Center (NOAA/CPC). Os scripts que prepararam os dados estão em `preparacao/` (rodam
no computador do orientador, com acesso ao Google Earth Engine).

**Estações em destaque (Oeste).** Santa Helena (2454012), Cascavel (2453056), Foz do Iguaçu (2554002) e Mercedes
(2454015) são usadas nos exemplos e nas figuras de série temporal. Mercedes substitui Marechal Cândido Rondon, do
projeto, porque nenhuma estação de Marechal cobre 1981–2020; ela fica a 15 km e em altitude parecida. O restante do estado entra nos mapas e nas tabelas por região.

---

## Como o trabalho roda no Colab

**Todas as análises rodam no Google Colab**, no navegador, sem instalar nada no computador.

### O repositório do projeto

```
github.com/fcoliveira-utfpr/spi_oni_pr
├── planejamento.md            este documento
├── dados/                     dados prontos (ver "Os dados")
├── src/
│   ├── fdp.py                 ajuste das 4 distribuições e testes de aderência
│   ├── spi.py                 SPI com a distribuição escolhida; eventos de seca
│   ├── enos.py                fases e intensidade do ENOS a partir do ONI
│   └── estatistica.py         correlação com bootstrap em blocos, contingência, Kruskal-Wallis
├── notebooks/                 00 = caderno de aprendizagem; 01 a 08 = notebooks do TCC
└── preparacao/                como os dados foram baixados (só para o orientador)
```

### A célula 0 de cada notebook

Todo notebook começa com a mesma célula. **Rode-a sempre primeiro**, toda vez que abrir o notebook. Ela:

1. baixa as funções da pasta `src/` do GitHub;
2. define o endereço dos dados (`DADOS`), que são lidos direto do GitHub;
3. conecta o seu **Google Drive** e cria a pasta `spi_oni_pr/resultados`.

```python
DADOS = "https://raw.githubusercontent.com/fcoliveira-utfpr/spi_oni_pr/main/dados/"

chuva = pd.read_csv(DADOS + "chuva_mensal_pr.csv")      # lê o arquivo direto da internet
```

- **O Colab apaga tudo quando a sessão fecha.** Por isso cada etapa grava os resultados no Drive (`SAIDA`), e a etapa
  seguinte lê de lá. A partir da Etapa 5, os notebooks dependem dos arquivos gravados pelos anteriores.

### Regras de trabalho

- **Rode as células em ordem**, de cima para baixo. Se algo der um erro estranho, use *Ambiente de execução →
  Reiniciar e executar tudo*.
- **Não edite o notebook original.** Use *Arquivo → Salvar uma cópia no Drive* e trabalhe na cópia.
- **Escreva, em células de texto, o que você entendeu de cada resultado.** Isso vira o rascunho do TCC2.
- **Exercícios**: cada notebook termina com perguntas. Responda na célula vazia logo abaixo.
- **Erro é normal.** Leia a última linha da mensagem de erro. Antes de pedir ajuda, tente entender o que ela diz;
  depois, mande ao orientador o print do erro e o que você tentou.

---

## Caderno de aprendizagem

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fcoliveira-utfpr/spi_oni_pr/blob/main/notebooks/00_aprendizagem.ipynb)

**Objetivo.** Aprender, com exemplos pequenos e com a chuva de Santa Helena, cada ideia e cada ferramenta que os
notebooks do TCC usam, antes de rodá-los para o estado inteiro.

É **um único notebook**, com um capítulo para cada notebook do TCC. Em cada capítulo há itens **resolvidos** (rode,
leia e mude os valores) e itens **para pensar e resolver** (responda com código ou com texto).

| Capítulo | O que ensina | Prepara para |
|---|---|---|
| 1 | Colab, variáveis, listas, `for`, `if` e funções com chuva diária | Etapa 1 |
| 2 | pandas: ler uma tabela, filtrar, somar por mês e por ano, média e desvio padrão | Etapa 2 |
| 3 | Tendência "na mão": contar pares que sobem e que descem (a ideia do Mann-Kendall) | Etapa 3 |
| 4 | Histograma, uma distribuição ajustada por cima dele, probabilidade acumulada | Etapa 4 |
| 5 | SPI de um mês feito à mão: chuva → probabilidade → desvio padrão | Etapa 5 |
| 6 | Média móvel de 3 meses e a regra dos 5 trimestres seguidos | Etapa 6 |
| 7 | Correlação, por que a autocorrelação engana e tabela de contingência com números simples | Etapa 7 |

**Entregar.** O caderno com todos os itens "para pensar e resolver" respondidos. Eles são a pauta das reuniões.

---

## Etapa 1. Colab e Python básico

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fcoliveira-utfpr/spi_oni_pr/blob/main/notebooks/01_python_basico.ipynb)

**Objetivo.** Aprender o mínimo de Python para seguir o trabalho: o que é uma célula, como rodar, como ler uma tabela e
fazer um gráfico.

**O que o notebook faz.**

1. O Colab: células de texto e de código, rodar, salvar uma cópia no Drive;
2. Variáveis e contas (chuva de um dia, soma de uma semana);
3. Listas e o laço `for` (chuva acumulada de um mês);
4. Decisões com `if` (dia chuvoso ou seco, limiar de 1 mm);
5. Funções (classificar o SPI pelas faixas de McKee);
6. Tabelas com pandas (chuva diária de Santa Helena) e o primeiro gráfico.

**Trecho explicado: uma função**

```python
def classe_spi(valor):
    if valor >= 2.0:
        return "Extremamente úmido"
    elif valor >= 1.5:
        return "Muito úmido"
    ...
```

`def` cria uma função: uma receita que recebe um valor e devolve uma resposta com `return`. O `if` / `elif` testa as
faixas da Tabela 1 do projeto, de cima para baixo, e para na primeira que for verdadeira.

**Entregar.** Os exercícios resolvidos e o gráfico da chuva mensal de Santa Helena em 2019.

---

## Etapa 2. Conhecendo os dados de chuva

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fcoliveira-utfpr/spi_oni_pr/blob/main/notebooks/02_dados_chuva.ipynb)

**Objetivo.** Saber com que dados o trabalho é feito: quantas estações, onde estão, quanto chove e como a chuva varia
ao longo do ano e entre as regiões.

**O que o notebook faz.**

1. Lê as estações e faz o mapa do Paraná com as estações coloridas pela mesorregião;
2. Resume a qualidade: % de dias preenchidos por estação (histograma e mapa);
3. Calcula a chuva anual média e o regime mensal (normal climatológica 1981–2010) de cada estação;
4. Compara o regime mensal das mesorregiões e das 4 estações em destaque;
5. Calcula a variabilidade: desvio padrão e coeficiente de variação (CV) de cada mês.

**Trecho explicado: total anual**

```python
anual = chuva.groupby(["cod", "ano"])["chuva_mm"].sum()     # soma os 12 meses de cada estação em cada ano
```

`groupby` junta as linhas que têm o mesmo código de estação e o mesmo ano; `.sum()` soma a chuva dentro de cada grupo.

**O que observar.** O Oeste e o Sudoeste chovem mais que o Norte; o Norte tem inverno seco marcado e o Sul tem chuva
bem distribuída. O CV é maior nos meses de inverno. Confira se isso aparece e compare com Aparecido et al. (2016).

**Entregar.** Mapa das estações, tabela com as estações em destaque e figura do regime mensal por mesorregião.

**O que escrever.** TCC2, Material e Métodos: área de estudo e dados (número de estações, período, fonte, critério de
seleção). Resultados: o primeiro parágrafo, caracterizando o regime de chuvas.

---

## Etapa 3. Homogeneidade e tendência

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fcoliveira-utfpr/spi_oni_pr/blob/main/notebooks/03_homogeneidade.ipynb)

**Objetivo.** Antes de calcular o SPI, conferir se as séries são homogêneas (sem "degraus" por troca de equipamento ou
de local) e se têm tendência. O SPI supõe que o clima de 1981 é comparável ao de 2020.

**O que o notebook faz.**

1. Teste de Pettitt na chuva anual de cada estação: há um ponto de mudança? Em que ano?
2. Teste de Mann-Kendall e inclinação de Sen: há tendência? De quantos mm por década?
3. Mapas: estações com ponto de mudança e com tendência significativa (5%).

**O que observar.** Algumas estações terão ponto de mudança. Se forem poucas e espalhadas, é provavelmente um problema
da estação; se houver um padrão regional, pode ser clima. Leve a lista para a reunião (ponto de decisão).

**Entregar.** Tabela-resumo dos testes e os dois mapas.

**O que escrever.** Material e Métodos (testes) e um parágrafo de Resultados.

---

## Etapa 4. Ajuste das distribuições de probabilidade

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fcoliveira-utfpr/spi_oni_pr/blob/main/notebooks/04_ajuste_fdp.ipynb)

**Objetivo.** Escolher a distribuição que descreve bem a chuva acumulada em 3 e em 12 meses. O SPI depende dessa
escolha: uma distribuição ruim nas caudas erra justamente as secas e os excessos.

**O que o notebook faz.**

1. Monta as chuvas acumuladas em 3 e 12 meses (somas móveis);
2. Para **cada estação, cada escala e cada mês do ano** (o SPI é sempre ajustado mês a mês), ajusta Gama, Gumbel,
   Log-Normal e Exponencial por máxima verossimilhança;
3. Avalia cada ajuste pelos testes de Kolmogorov-Smirnov e Anderson-Darling (5%) e pelo critério de informação de
   Akaike (AIC);
4. Resume: em quantos % dos casos cada distribuição é aprovada e é a melhor; mapa da melhor distribuição por estação;
5. Mostra, para Santa Helena, o histograma com as 4 curvas por cima (figura do TCC).

**Trecho explicado: ajustar uma distribuição**

```python
from scipy import stats
parametros = stats.gamma.fit(dados, floc=0)      # máxima verossimilhança; floc=0 fixa o início da curva em zero
p_valor = stats.kstest(dados, "gamma", args=parametros).pvalue
```

**Cuidados que o notebook explica.**

- **Meses com chuva zero.** Gama e Log-Normal só aceitam valores maiores que zero. Se houver zeros, usa-se a
  distribuição mista: a probabilidade de zero (q) à parte e a distribuição ajustada só aos valores positivos
  (Guttman, 1999). No Paraná isso é raro no acumulado de 3 meses e não ocorre no de 12.
- **KS com parâmetros estimados.** Quando os parâmetros são estimados dos próprios dados, o KS clássico fica
  "bonzinho" demais. O notebook mostra a correção por simulação (Monte Carlo) nas estações em destaque.

**Entregar.** Tabela com a % de aprovação e a % de "melhor ajuste" de cada distribuição, por escala, e a figura de
Santa Helena.

**O que escrever.** Resultados e Discussão, item 1 (ajuste das FDPs). Compare com Blain e Meschiatti (2014) e com
Oliveira et al. (2025).

---

## Etapa 5. Cálculo do SPI-3 e do SPI-12

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fcoliveira-utfpr/spi_oni_pr/blob/main/notebooks/05_spi.ipynb)

**Objetivo.** Calcular o SPI com a distribuição escolhida na Etapa 4 e caracterizar as secas e os excessos.

**O que o notebook faz.**

1. Calcula o SPI-3 e o SPI-12 de todas as estações;
2. Confere o resultado com a função `spi` da biblioteca `agrometeorologiapy` (distribuição Gama), em Santa Helena;
3. Classifica cada mês pelas faixas de McKee et al. (1993);
4. Identifica os **eventos de seca** (SPI ≤ −1 por pelo menos 1 mês): início, fim, duração, severidade (soma do SPI) e
   pico; o mesmo para os excessos (SPI ≥ +1);
5. Figura da série do SPI-3 e do SPI-12 das 4 estações em destaque;
6. Mapa do SPI nos anos mais secos e mais chuvosos da série, identificados pelo próprio notebook; confira cada um
   com os registros de quebra de safra (DERAL/SEAB).

**Trecho explicado: o SPI de um valor**

```python
F = stats.gamma.cdf(chuva_3meses, *parametros)    # probabilidade de chover até esse valor (0 a 1)
spi = stats.norm.ppf(F)                           # o mesmo "lugar" na curva normal padrão
```

O SPI transforma a chuva em uma régua comum: SPI = −1,5 quer dizer "tão seco quanto acontece só em 7% dos anos",
em qualquer lugar e em qualquer mês.

**O que observar.** A média do SPI de cada estação deve ficar perto de 0 e o desvio padrão perto de 1. Confira.

**Entregar.** Arquivo `spi_pr.csv` gravado no Drive, tabela de eventos de seca das 4 estações e a figura das séries.

**O que escrever.** Resultados e Discussão, item 2 (SPI, secas e excessos).

---

## Etapa 6. Classificação do ENOS pelo ONI

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fcoliveira-utfpr/spi_oni_pr/blob/main/notebooks/06_oni_enos.ipynb)

**Objetivo.** Saber, para cada mês de 1981 a 2020, se o Pacífico estava em El Niño, La Niña ou Neutro, e com que
intensidade.

**O que o notebook faz.**

1. Lê o ONI e faz o gráfico de barras vermelhas (positivo) e azuis (negativo);
2. Aplica a regra do NOAA: ±0,5 °C por pelo menos 5 trimestres seguidos;
3. Monta a lista dos eventos: início, fim, duração, pico e intensidade (fraco, moderado, forte, muito forte);
4. Confere a lista com a tabela oficial do NOAA/CPC;
5. Grava `enos_mensal.csv` (fase e intensidade de cada mês).

**O que observar.** De 1981 a 2020 devem aparecer, entre outros, os El Niños muito fortes de 1982/83, 1997/98 e 2015/16 e as La
Niñas fortes de 1988/89, 1999/2000 e 2010/11.

**Entregar.** Tabela dos eventos e o gráfico do ONI.

**O que escrever.** Material e Métodos (item 4.5 do projeto, já escrito, ajustar) e o início do item 3 dos Resultados.

---

## Etapa 7. Relação entre SPI e ENOS

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fcoliveira-utfpr/spi_oni_pr/blob/main/notebooks/07_spi_x_enos.ipynb)

**Objetivo.** Responder à pergunta do trabalho, de forma visual e numérica.

**O que o notebook faz.**

*Parte A, visual (estações em destaque):*

1. Série do SPI-3 e do SPI-12 com faixas vermelhas (El Niño) e azuis (La Niña);
2. Dispersão ONI × SPI-3, um painel por estação do ano;
3. Mapa de calor da correlação ONI × SPI-3: mês do ano (linhas) × defasagem de 0 a 12 meses (colunas).

*Parte B, numérica (todas as estações):*

4. **Correlação por estação do ano.** ONI de SON × SPI-3 de novembro (chuva de SON), e assim para DJF, MAM e JJA;
   Pearson e Spearman. A significância é dada pelo **bootstrap em blocos**, que respeita a autocorrelação;
5. **Correlação defasada** do SPI-12 com o ONI;
6. **Tabela de contingência** fase do ENOS × classe do SPI (seco ≤ −1; normal; úmido ≥ +1), teste qui-quadrado,
   **probabilidade condicional** P(seco | La Niña), P(úmido | El Niño) e **risco relativo** em relação à climatologia;
7. **Kruskal-Wallis + Dunn**: o SPI difere entre El Niño, Neutro e La Niña? E entre as intensidades (fraco a muito
   forte)? Isso testa o "efeito dose-resposta";
8. **Mapas do Paraná**: correlação na primavera e no inverno, P(seca | La Niña) e P(excesso | El Niño), estação por
   estação; resumo por mesorregião.

**Trecho explicado: por que bootstrap em blocos**

O SPI-12 de um mês é quase igual ao do mês anterior: os dois têm 11 meses em comum. Em 40 anos há 480 valores, mas
muito menos que 480 informações independentes. O teste t "acredita" que são 480 e acha correlação significativa com
facilidade. O bootstrap em blocos sorteia **pedaços** da série (por exemplo, de 12 meses), mantendo a dependência
dentro de cada pedaço, e vê quantas vezes uma correlação daquele tamanho aparece por acaso.

**O que observar.** A literatura indica sinal mais forte na primavera (SON) do ano de início do El Niño e no fim do
outono e inverno do ano seguinte, mais intenso no Sul e no Oeste do que no Norte (Grimm et al., 2000; de Bodas Terassi
et al., 2018). Veja se os mapas mostram isso.

**Entregar.** As figuras A1 a A3, as tabelas B4 a B7 e os mapas B8.

**O que escrever.** Resultados e Discussão, item 3, o núcleo do trabalho. Para cada resultado: o que foi encontrado,
o número, e se concorda ou não com a literatura e por quê.

---

## Etapa 8. Figuras e tabelas finais

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fcoliveira-utfpr/spi_oni_pr/blob/main/notebooks/08_figuras_tcc.ipynb)

**Objetivo.** Refazer, com padrão único (fonte, cores, 300 dpi), as figuras e tabelas que vão para o TCC2.

**Entregar.** Pasta `figuras_tcc/` no Drive, com as figuras numeradas na ordem em que aparecem no texto.

---

## Etapa 9. Escrita do TCC2

O texto é escrito no [Google Docs do TCC2](https://docs.google.com/document/d/1P9D4LkLHdXI7kn__TAf4QvMt8qKqxE0d4CG8fD0DBH8/edit?usp=sharing),
que já tem a formatação da UTFPR e o conteúdo do projeto. Em cada tópico há:

- **texto em azul e itálico**: orientação do que escrever. Apague à medida que escrever;
- **texto em preto**: texto do projeto, já adaptado, que pode ser mantido ou melhorado.

### Ordem de escrita

1. **Material e Métodos**: passar do futuro para o passado ("foram utilizadas") e ajustar ao que foi feito de verdade;
2. **Resultados e Discussão**: um item por etapa (4, 5, 6 e 7), escrito logo depois de cada etapa;
3. **Conclusões**: respostas diretas aos objetivos específicos, uma por objetivo;
4. **Introdução e Referencial**: revisar à luz dos resultados (o que ficou mais importante?);
5. **Resumo e abstract**: por último.

### Regras de estilo

- **Sem primeira pessoa**: "neste trabalho", "nesta pesquisa".
- **Toda afirmação tem citação**, ao final do parágrafo: (DE BODAS TERASSI et al., 2018).
- **Todo resultado tem número**: "a correlação na primavera variou de 0,25 a 0,55", não "a correlação foi alta".
- **Figuras e tabelas citadas no texto antes de aparecerem**, numeradas na ordem.
- **Quando faltar um número, deixe o marcador** [INSERIR VALOR]. Nunca invente.

---

## Pontos de decisão com o orientador

| Após a etapa | Decisão |
|---|---|
| 2 | ~~Limite de dias preenchidos e estação de Marechal Cândido Rondon~~ decidido: 10% e Mercedes (2454015) |
| 3 | O que fazer com estações não homogêneas (excluir, manter e anotar) |
| 4 | Uma distribuição por escala para o estado inteiro ou a melhor de cada estação |
| 5 | Período de referência do SPI (1981–2010 ou a série inteira) |
| 7 | Tamanho do bloco do bootstrap; defasagens que entram no texto |
| 9 | Título definitivo (Paraná ou Oeste do Paraná) e se vira artigo |

## Riscos e o que fazer

| Risco | Como lidar |
|---|---|
| Nenhuma distribuição aprovada em alguns meses | usar a de menor AIC e registrar; discutir a cauda |
| Correlação fraca no Norte do estado | é esperado (zona de transição); é resultado, não problema |
| Colab desconecta no meio da Etapa 4 | os resultados são gravados no Drive por estação; rodar de novo pula as prontas |
| Estações em destaque com ponto de mudança | trocar por uma vizinha da mesma região |

## Referências de base

Já estão nas referências do projeto, salvo indicação.

- BLAIN, G. C.; MESCHIATTI, M. C., 2014.
- DE BODAS TERASSI, P. M. et al. *International Journal of Climatology*, 2018.
- GRIMM, A. M.; BARROS, V. R.; DOYLE, M. E. Climate variability in southern South America associated with El Niño
  and La Niña events. *Journal of Climate*, 2000. [incluir]
- GUTTMAN, N. B., 1999.
- MCKEE, T. B.; DOESKEN, N. J.; KLEIST, J., 1993.
- OLIVEIRA, F. C. et al. *Revista Brasileira de Geografia Física*, 2025.
- TRENBERTH, K. E., 1997.
- WMO. *Standardized Precipitation Index User Guide*, 2012.
- WILKS, D. S. *Statistical Methods in the Atmospheric Sciences* (bootstrap em blocos e contingência). [incluir]
- XAVIER, A. C. et al. New improved Brazilian daily weather gridded data (1961–2020). *International Journal of
  Climatology*, 2022. [incluir]
