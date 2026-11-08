"""Índice de Precipitação Padronizada (SPI; McKee, Doesken e Kleist, 1993; Guttman, 1999).

Passos:
  1) somar a chuva em janelas móveis de `escala` meses (SPI-3: o mês e os dois anteriores);
  2) para cada mês do calendário (janeiro, fevereiro, ...), ajustar a distribuição aos totais de todos os anos;
  3) transformar a probabilidade acumulada de cada total no valor da normal padrão: SPI = Φ⁻¹(H(x)).
"""
import numpy as np
import pandas as pd
from scipy import stats

import fdp

# limite da probabilidade, para o SPI não ir a ±infinito quando H = 0 ou H = 1
EPS = 1e-6


def serie_da_estacao(mensal, cod):
    """Chuva mensal de uma estação, em ordem de data, com as colunas ano, mes e chuva_mm."""
    s = mensal[mensal["cod"] == cod].sort_values(["ano", "mes"]).reset_index(drop=True)
    return s[["ano", "mes", "chuva_mm"]]


def acumular(chuva, escala):
    """Soma móvel de `escala` meses. Os primeiros `escala - 1` meses ficam vazios (NaN)."""
    return chuva.rolling(escala).sum()


def calcular_spi(serie, escala, distribuicao="Gama", ano_ini=None, ano_fim=None):
    """SPI de uma estação.

    serie: tabela com ano, mes e chuva_mm (de `serie_da_estacao`).
    escala: 3 ou 12 (meses).
    distribuicao: "Gama", "Gumbel", "Log-Normal" ou "Exponencial".
    ano_ini, ano_fim: período de referência do ajuste (None = a série inteira).

    Devolve a tabela com as colunas ano, mes, acumulado e spi.
    """
    tab = serie.copy()
    tab["acumulado"] = acumular(tab["chuva_mm"], escala)
    tab["spi"] = np.nan

    for m in range(1, 13):                                   # um ajuste para cada mês do calendário
        do_mes = tab["mes"] == m
        referencia = tab[do_mes]
        if ano_ini is not None:
            referencia = referencia[(referencia["ano"] >= ano_ini) & (referencia["ano"] <= ano_fim)]
        valores = referencia["acumulado"].dropna()
        q = fdp.prob_zero(valores)                           # proporção de totais iguais a zero
        parametros = fdp.ajustar(valores, distribuicao)

        x = tab.loc[do_mes, "acumulado"]
        h = fdp.prob_acumulada(x, distribuicao, parametros, q)
        h = np.clip(h, EPS, 1 - EPS)                         # evita 0 e 1 exatos
        tab.loc[do_mes, "spi"] = stats.norm.ppf(h)           # Φ⁻¹: inversa da normal padrão
    return tab


def classe_spi(valor):
    """Classe de McKee, Doesken e Kleist (1993) para um valor de SPI."""
    if pd.isna(valor):
        return None
    if valor >= 2.0:
        return "Extremamente úmido"
    elif valor >= 1.5:
        return "Muito úmido"
    elif valor >= 1.0:
        return "Moderadamente úmido"
    elif valor > -1.0:
        return "Normal"
    elif valor > -1.5:
        return "Moderadamente seco"
    elif valor > -2.0:
        return "Severamente seco"
    else:
        return "Extremamente seco"


def classe3(valor):
    """Três classes usadas na relação com o ENOS: seco (SPI ≤ −1), normal, úmido (SPI ≥ +1)."""
    if pd.isna(valor):
        return None
    if valor <= -1.0:
        return "seco"
    if valor >= 1.0:
        return "úmido"
    return "normal"


def eventos(tab, tipo="seca", limiar=1.0):
    """Eventos de seca (SPI ≤ −limiar) ou de excesso (SPI ≥ +limiar) pela teoria das sequências.

    Um evento começa no primeiro mês que passa do limiar e termina no último mês seguido nessa condição.
    Devolve uma tabela com início, fim, duração (meses), severidade (soma do SPI) e pico.
    """
    lista = []
    dentro = False                       # estamos dentro de um evento?
    for i, linha in tab.iterrows():
        valor = linha["spi"]
        if pd.isna(valor):
            condicao = False
        elif tipo == "seca":
            condicao = valor <= -limiar
        else:
            condicao = valor >= limiar

        if condicao and not dentro:      # começa um evento
            dentro = True
            inicio = (int(linha["ano"]), int(linha["mes"]))
            valores = [valor]
        elif condicao and dentro:        # o evento continua
            valores.append(valor)
        elif not condicao and dentro:    # o evento terminou no mês anterior
            dentro = False
            lista.append(_resumo(inicio, fim, valores, tipo))
        if condicao:
            fim = (int(linha["ano"]), int(linha["mes"]))
    if dentro:                           # evento ainda aberto no fim da série
        lista.append(_resumo(inicio, fim, valores, tipo))
    return pd.DataFrame(lista, columns=["inicio", "fim", "duracao_meses", "severidade", "pico"])


def _resumo(inicio, fim, valores, tipo):
    pico = min(valores) if tipo == "seca" else max(valores)
    return {"inicio": f"{inicio[1]:02d}/{inicio[0]}", "fim": f"{fim[1]:02d}/{fim[0]}",
            "duracao_meses": len(valores), "severidade": round(sum(valores), 2), "pico": round(pico, 2)}
