"""Fases e intensidade do El Niño-Oscilação Sul (ENOS) pelo Oceanic Niño Index (ONI) da NOAA/CPC.

Regra: El Niño quando o ONI ≥ +0,5 °C por pelo menos 5 trimestres móveis seguidos; La Niña quando o ONI ≤ −0,5 °C
pelo mesmo critério; os demais meses são neutros. Intensidade pelo valor extremo do ONI no evento:
fraca (0,5 a 0,9), moderada (1,0 a 1,4), forte (1,5 a 1,9) e muito forte (≥ 2,0).
"""
import pandas as pd

LIMIAR = 0.5
MINIMO_TRIMESTRES = 5


def oni_mensal(oni):
    """Tabela do ONI com um valor por mês: cada trimestre móvel é atribuído ao mês central (DJF -> janeiro)."""
    tab = oni.rename(columns={"mes_central": "mes"})[["ano", "mes", "trimestre", "oni"]].copy()
    return tab.sort_values(["ano", "mes"]).reset_index(drop=True)


def intensidade(pico):
    """Classe de intensidade pelo valor extremo (absoluto) do ONI no evento."""
    p = abs(round(pico, 1))   # o ONI é publicado com uma casa decimal
    if p >= 2.0:
        return "muito forte"
    elif p >= 1.5:
        return "forte"
    elif p >= 1.0:
        return "moderada"
    else:
        return "fraca"


def classificar(tab):
    """Acrescenta as colunas fase (El Niño, La Niña, Neutro), evento (número) e intensidade.

    Percorre os meses e procura sequências seguidas acima de +0,5 ou abaixo de −0,5. Só as sequências com pelo
    menos 5 meses (trimestres móveis) viram evento.
    """
    tab = tab.copy()
    tab["fase"] = "Neutro"
    tab["evento"] = 0
    tab["intensidade"] = ""

    valores = list(tab["oni"])
    n = len(valores)
    numero = 0
    i = 0
    while i < n:
        if valores[i] >= LIMIAR:
            sinal = "El Niño"
        elif valores[i] <= -LIMIAR:
            sinal = "La Niña"
        else:
            i = i + 1
            continue
        # anda enquanto o ONI continuar do mesmo lado do limiar
        j = i
        while j < n and ((sinal == "El Niño" and valores[j] >= LIMIAR) or (sinal == "La Niña" and valores[j] <= -LIMIAR)):
            j = j + 1
        if j - i >= MINIMO_TRIMESTRES:             # sequência longa o bastante: é um evento
            numero = numero + 1
            trecho = valores[i:j]
            pico = max(trecho) if sinal == "El Niño" else min(trecho)
            linhas = tab.index[i:j]
            tab.loc[linhas, "fase"] = sinal
            tab.loc[linhas, "evento"] = numero
            tab.loc[linhas, "intensidade"] = intensidade(pico)
        i = j
    return tab


def lista_eventos(tab):
    """Uma linha por evento: fase, início, fim, duração, ONI de pico e intensidade."""
    linhas = []
    for numero in sorted(tab["evento"].unique()):
        if numero == 0:
            continue
        ev = tab[tab["evento"] == numero]
        fase = ev["fase"].iloc[0]
        pico = ev["oni"].max() if fase == "El Niño" else ev["oni"].min()
        linhas.append({"fase": fase,
                       "inicio": f"{ev['trimestre'].iloc[0]} {ev['ano'].iloc[0]}",
                       "fim": f"{ev['trimestre'].iloc[-1]} {ev['ano'].iloc[-1]}",
                       "duracao_meses": len(ev), "oni_pico": pico, "intensidade": ev["intensidade"].iloc[0]})
    return pd.DataFrame(linhas)
