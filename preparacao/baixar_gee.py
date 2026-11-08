"""Baixa do Google Earth Engine os dados de chuva do Paraná usados no projeto.

Roda só no computador do orientador (precisa de acesso ao GEE). O aluno usa os arquivos já prontos em dados/.

1) Pluviômetros observados (ANA, INMET e redes estaduais; Xavier et al., 2022), série diária com falhas preenchidas
   pela grade BR-DWGD: asset projects/fcoliveira/assets/observados_inmet/pr, filtrado para uf == 'PR'.
2) Só entram as estações com série de 01/1981 a 07/2020 (fim do asset); a seleção final (falhas na janela) é feita
   em montar_dados.py.

Saídas (brutos, fora do git): preparacao/brutos/obs/<cod>.csv.gz
Uso: python preparacao/baixar_gee.py
"""
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import ee
import pandas as pd

PROJETO = "fcoliveira"
OBS = "projects/fcoliveira/assets/observados_inmet/pr"
PASTA = Path(__file__).resolve().parent / "brutos"
INV = PASTA / "estacoes_pr_inventario.csv"


def tentar(f, n=5):
    for k in range(n):
        try:
            return f()
        except Exception as e:  # limite de taxa / memória: espera e tenta de novo
            if k == n - 1:
                raise
            time.sleep(10 * (k + 1))


def baixar_estacao(cod):
    arq = PASTA / "obs" / f"{cod}.csv.gz"
    if arq.exists():
        return
    fc = (ee.FeatureCollection(OBS).filter(ee.Filter.eq("uf", "PR")).filter(ee.Filter.eq("cod_estacao", str(cod)))
          .select(["data", "valor", "preenchido"], None, False))
    df = tentar(lambda: ee.data.computeFeatures({"expression": fc, "fileFormat": "PANDAS_DATAFRAME"}))
    df = df[["data", "valor", "preenchido"]].sort_values("data")
    df.to_csv(arq, index=False)


if __name__ == "__main__":
    ee.Initialize(project=PROJETO)
    (PASTA / "obs").mkdir(parents=True, exist_ok=True)
    inv = pd.read_csv(INV, dtype={"cod": str})
    inv = inv[(inv["ini"] <= "1981-01-31") & (inv["fim"] >= "2020-07-01")]

    with ThreadPoolExecutor(16) as ex:
        list(ex.map(baixar_estacao, inv["cod"]))
    print("observados: ok", flush=True)

