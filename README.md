# spi_oni_pr

**Índice de Precipitação Padronizada no estado do Paraná associado aos eventos de El Niño-Oscilação Sul**

Trabalho de conclusão de curso de Agronomia, UTFPR Campus Santa Helena.
Aluno: Eduardo de Carvalho Ritchie. Orientador: Prof. Dr. Fabrício Correia de Oliveira.

---

## A pesquisa em poucas linhas

A chuva do Paraná varia muito de um ano para outro, e parte dessa variação vem do Oceano Pacífico: o **El Niño**
tende a deixar o Sul do Brasil mais chuvoso e a **La Niña**, mais seco. Esta pesquisa mede essa relação em 370
pluviômetros do Paraná, de 1981 a 2020.

```
SPI-3   seca ou excesso de chuva em 3 meses   (seca agrícola; casa com as estações do ano)
SPI-12  seca ou excesso de chuva em 12 meses  (seca hidrológica)
ONI     temperatura do Pacífico (Niño 3.4)    → El Niño, Neutro ou La Niña, e a intensidade
```

A relação SPI × ENOS é mostrada de forma **visual** (séries com as fases, dispersão, mapa de calor mês × defasagem,
mapas do Paraná) e **numérica** (correlação por estação do ano com bootstrap em blocos, probabilidade de seca e de
excesso condicionada à fase do ENOS, Kruskal-Wallis entre fases e intensidades).

O roteiro completo está em **[planejamento.md](planejamento.md)**.

---

## Por onde começar

1. Leia o [planejamento.md](planejamento.md), principalmente "A pesquisa em uma página" e "Os dados".
2. Faça o **caderno de aprendizagem** (`00_aprendizagem`, primeira linha da tabela abaixo).
3. Depois, abra o notebook 01 pelo link do Colab, faça **Arquivo → Salvar uma cópia no Drive** e siga os notebooks
   do TCC em ordem. A partir do 05, cada um depende dos resultados do anterior.

---

## Estrutura dos arquivos

```
spi_oni_pr/
├── README.md                     este arquivo
├── planejamento.md               roteiro do trabalho: etapas, código explicado, o que entregar e escrever
│
├── dados/                        dados prontos; os notebooks leem direto do GitHub
│   ├── estacoes_pr.csv           370 pluviômetros: código, município, mesorregião, lat, lon, altitude,
│   │                             % de dias preenchidos e estações em destaque
│   ├── chuva_mensal_pr.csv       chuva mensal (mm) de cada estação, 01/1981 a 07/2020
│   ├── chuva_diaria_destaque.csv chuva diária das 4 estações em destaque do Oeste
│   ├── oni.csv                   Oceanic Niño Index (NOAA/CPC), 1950 em diante
│   ├── pr_mesorregioes.geojson   limites das mesorregiões (IBGE), para os mapas
│   └── pr_municipios.geojson     limites dos municípios (IBGE)
│
├── src/                          funções do projeto, comentadas, usadas pelos notebooks
├── notebooks/                    00 = caderno de aprendizagem; 01 a 08 = notebooks do TCC
└── preparacao/                   como os dados foram baixados e montados (roda só no computador do orientador)
```

---

## Notebooks

| Etapa | Notebook | O que faz |
|---|---|---|
| antes | [00_aprendizagem](https://colab.research.google.com/github/fcoliveira-utfpr/spi_oni_pr/blob/main/notebooks/00_aprendizagem.ipynb) | Caderno de aprendizagem: um capítulo por notebook do TCC |
| 1 | [01_python_basico](https://colab.research.google.com/github/fcoliveira-utfpr/spi_oni_pr/blob/main/notebooks/01_python_basico.ipynb) | Colab e Python básico com chuva de Santa Helena |
| 2 | [02_dados_chuva](https://colab.research.google.com/github/fcoliveira-utfpr/spi_oni_pr/blob/main/notebooks/02_dados_chuva.ipynb) | Estações, qualidade, regime mensal e variabilidade |
| 3 | [03_homogeneidade](https://colab.research.google.com/github/fcoliveira-utfpr/spi_oni_pr/blob/main/notebooks/03_homogeneidade.ipynb) | Pettitt, Mann-Kendall e Sen |
| 4 | [04_ajuste_fdp](https://colab.research.google.com/github/fcoliveira-utfpr/spi_oni_pr/blob/main/notebooks/04_ajuste_fdp.ipynb) | Gama, Gumbel, Log-Normal e Exponencial; KS, AD e AIC |
| 5 | [05_spi](https://colab.research.google.com/github/fcoliveira-utfpr/spi_oni_pr/blob/main/notebooks/05_spi.ipynb) | SPI-3 e SPI-12, classes de McKee, eventos de seca e excesso |
| 6 | [06_oni_enos](https://colab.research.google.com/github/fcoliveira-utfpr/spi_oni_pr/blob/main/notebooks/06_oni_enos.ipynb) | Fases e intensidade do ENOS pelo ONI |
| 7 | [07_spi_x_enos](https://colab.research.google.com/github/fcoliveira-utfpr/spi_oni_pr/blob/main/notebooks/07_spi_x_enos.ipynb) | Relação SPI × ENOS: visual e numérica |
| 8 | [08_figuras_tcc](https://colab.research.google.com/github/fcoliveira-utfpr/spi_oni_pr/blob/main/notebooks/08_figuras_tcc.ipynb) | Figuras e tabelas finais em 300 dpi |

Cada notebook grava seus resultados no Drive (`spi_oni_pr/resultados`); a partir do 05, cada um lê o que o anterior gravou.
Rodando em sequência, os nove levam cerca de 10 minutos no Colab.

O código dos notebooks é escrito da forma mais simples possível, para quem nunca programou: cada bloco tem uma
explicação antes e comentários linha a linha. Os dados são lidos direto do GitHub, sem baixar nada:

```python
DADOS = "https://raw.githubusercontent.com/fcoliveira-utfpr/spi_oni_pr/main/dados/"
chuva = pd.read_csv(DADOS + "chuva_mensal_pr.csv")
```

---

## Fontes dos dados

- **Chuva:** pluviômetros da ANA, do INMET e das redes estaduais usados por Xavier et al. (2022), com as falhas
  diárias preenchidas pela grade BR-DWGD. Xavier, A. C.; Scanlon, B. R.; King, C. W.; Alves, A. I. New improved
  Brazilian daily weather gridded data (1961–2020). *International Journal of Climatology*, v. 42, n. 16,
  p. 8390-8404, 2022. https://doi.org/10.1002/joc.7731
- **Critério das estações:** série completa de 01/01/1981 a 31/07/2020 e no máximo 10% de dias preenchidos (exceção:
  Foz do Iguaçu 2554002, até 12/2019, estação em destaque).
- **ONI:** NOAA Climate Prediction Center, https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt
- **Malhas e mesorregiões:** IBGE, API de localidades e de malhas.
