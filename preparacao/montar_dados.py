"""Monta os arquivos de dados/ a partir dos brutos baixados por baixar_gee.py e das fontes da web.

Critério das estações: série de 01/01/1981 a 31/07/2020 completa no asset e no máximo 10% de dias preenchidos pelo
Xavier nessa janela. Exceção: Foz do Iguaçu 2554002, estação em destaque, que termina em 31/12/2019.

Brutos da web (preparacao/brutos/web/):
  oni.ascii.txt      https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt
  mun_pr.json        https://servicodados.ibge.gov.br/api/v1/localidades/estados/41/municipios
  pr_meso.geojson    https://servicodados.ibge.gov.br/api/v3/malhas/estados/41?intrarregiao=mesorregiao&formato=application/vnd.geo%2Bjson&qualidade=intermediaria
  pr_mun.geojson     https://servicodados.ibge.gov.br/api/v3/malhas/estados/41?intrarregiao=municipio&formato=application/vnd.geo%2Bjson&qualidade=intermediaria
Uso: python preparacao/montar_dados.py
"""
import json
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
BRUTOS = RAIZ / "preparacao" / "brutos"
DADOS = RAIZ / "dados"
INI, FIM = "1981-01-01", "2020-07-31"
LIMITE_PREENCHIDO = 0.10
DESTAQUE = {"2454012": "Santa Helena", "2453056": "Cascavel", "2554002": "Foz do Iguaçu",
            "2454015": "Mercedes (vizinha de Marechal Cândido Rondon)"}

DADOS.mkdir(exist_ok=True)

# --- municípios e mesorregiões do IBGE ---------------------------------------------------------------------------
mun = json.loads((BRUTOS / "web" / "mun_pr.json").read_text())
meso_de = {str(m["id"]): m["microrregiao"]["mesorregiao"]["nome"] for m in mun}
id_meso = {m["microrregiao"]["mesorregiao"]["nome"]: str(m["microrregiao"]["mesorregiao"]["id"]) for m in mun}
nome_mun = {str(m["id"]): m["nome"] for m in mun}

# --- estações ------------------------------------------------------------------------------------------------------
inv = pd.read_csv(BRUTOS / "estacoes_pr_inventario.csv", dtype={"cod": str, "cod_ibge": str})
linhas_mensais, linhas_est, diarias = [], [], []
for r in inv.itertuples():
    arq = BRUTOS / "obs" / f"{r.cod}.csv.gz"
    if not arq.exists():
        continue
    d = pd.read_csv(arq, parse_dates=["data"])
    d = d[(d["data"] >= INI) & (d["data"] <= FIM)]
    completa = len(d) == len(pd.date_range(INI, FIM))
    frac = d["preenchido"].mean()
    if not ((completa and frac <= LIMITE_PREENCHIDO) or r.cod in DESTAQUE):
        continue
    d["ano"], d["mes"] = d["data"].dt.year, d["data"].dt.month
    m = d.groupby(["ano", "mes"]).agg(chuva_mm=("valor", "sum"), dias=("valor", "size"),
                                      dias_preenchidos=("preenchido", "sum")).reset_index()
    m.insert(0, "cod", r.cod)
    linhas_mensais.append(m)
    linhas_est.append(dict(cod=r.cod, municipio=nome_mun.get(r.cod_ibge, r.municipio), cod_ibge=r.cod_ibge,
                           mesorregiao=meso_de[r.cod_ibge], lat=round(r.lat, 5), lon=round(r.lon, 5),
                           alt_m=r.alt, inicio=d["data"].min().date(), fim=d["data"].max().date(),
                           pct_preenchido=round(100 * frac, 2), destaque=DESTAQUE.get(r.cod, "")))
    if r.cod in DESTAQUE:
        diarias.append(d.assign(cod=r.cod)[["cod", "data", "valor", "preenchido"]]
                       .rename(columns={"valor": "chuva_mm"}))

est = pd.DataFrame(linhas_est).sort_values(["mesorregiao", "municipio", "cod"])
est.to_csv(DADOS / "estacoes_pr.csv", index=False)
mensal = pd.concat(linhas_mensais)
mensal["chuva_mm"] = mensal["chuva_mm"].round(1)
mensal.to_csv(DADOS / "chuva_mensal_pr.csv", index=False)
diaria = pd.concat(diarias)
diaria["data"] = diaria["data"].dt.date
diaria.to_csv(DADOS / "chuva_diaria_destaque.csv", index=False)
print(len(est), "estações;", len(mensal), "estação-meses;", len(diaria), "dias nas estações em destaque")
print(est["mesorregiao"].value_counts().to_string())

# --- ONI -----------------------------------------------------------------------------------------------------------
oni = pd.read_csv(BRUTOS / "web" / "oni.ascii.txt", sep=r"\s+")
trimestres = ["DJF", "JFM", "FMA", "MAM", "AMJ", "MJJ", "JJA", "JAS", "ASO", "SON", "OND", "NDJ"]
oni = pd.DataFrame({"ano": oni["YR"], "trimestre": oni["SEAS"],
                    "mes_central": [trimestres.index(s) + 1 for s in oni["SEAS"]], "oni": oni["ANOM"]})
oni.to_csv(DADOS / "oni.csv", index=False)
print("ONI:", oni["ano"].min(), "a", oni["ano"].max(), oni.iloc[-1]["trimestre"])

# --- malhas --------------------------------------------------------------------------------------------------------
meso = json.loads((BRUTOS / "web" / "pr_meso.geojson").read_text())
nome_meso = {v: k for k, v in id_meso.items()}
for f in meso["features"]:
    f["properties"]["mesorregiao"] = nome_meso[f["properties"]["codarea"]]
(DADOS / "pr_mesorregioes.geojson").write_text(json.dumps(meso, ensure_ascii=False))
munj = json.loads((BRUTOS / "web" / "pr_mun.geojson").read_text())
for f in munj["features"]:
    c = f["properties"]["codarea"]
    f["properties"].update(municipio=nome_mun[c], mesorregiao=meso_de[c])
(DADOS / "pr_municipios.geojson").write_text(json.dumps(munj, ensure_ascii=False))
print("malhas ok")
