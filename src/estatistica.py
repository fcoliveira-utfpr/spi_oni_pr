"""Testes estatísticos do trabalho, escritos de forma simples (laços em vez de atalhos).

- Pettitt (1979): ponto de mudança;
- Mann-Kendall (Mann, 1945; Kendall, 1975) e inclinação de Sen (1968): tendência;
- correlação com bootstrap em blocos (Wilks, 2011);
- tabela de contingência, probabilidade condicional e risco relativo;
- Kruskal-Wallis (1952) seguido do teste de Dunn (1964) com correção de Bonferroni.
"""
import numpy as np
import pandas as pd
from scipy import stats


# ------------------------------------------------------------------------------------------------------------------
# Homogeneidade e tendência
# ------------------------------------------------------------------------------------------------------------------
def pettitt(x):
    """Teste de Pettitt. Devolve (posição da mudança, estatística K, valor-p aproximado).

    A posição é o índice do último valor ANTES da mudança.
    """
    x = list(x)
    n = len(x)
    melhor_k, posicao = 0, 0
    for t in range(n - 1):                         # testa cada ponto possível de mudança
        u = 0
        for i in range(t + 1):                     # valores antes (até t)
            for j in range(t + 1, n):              # valores depois
                u = u + np.sign(x[j] - x[i])
        if abs(u) > melhor_k:
            melhor_k, posicao = abs(u), t
    p = 2 * np.exp(-6 * melhor_k ** 2 / (n ** 3 + n ** 2))
    return posicao, melhor_k, min(p, 1.0)


def mann_kendall(x):
    """Teste de Mann-Kendall. Devolve (S, Z, valor-p). S > 0: tendência de aumento; S < 0: de redução."""
    x = list(x)
    n = len(x)
    s = 0
    for i in range(n - 1):                         # compara cada par (i antes de j)
        for j in range(i + 1, n):
            s = s + np.sign(x[j] - x[i])           # +1 se subiu, −1 se desceu, 0 se igual
    var_s = n * (n - 1) * (2 * n + 5) / 18         # variância de S sem empates
    if s > 0:
        z = (s - 1) / np.sqrt(var_s)
    elif s < 0:
        z = (s + 1) / np.sqrt(var_s)
    else:
        z = 0.0
    p = 2 * (1 - stats.norm.cdf(abs(z)))           # bilateral
    return s, z, p


def sen(x):
    """Inclinação de Sen: mediana das inclinações entre todos os pares (unidade de x por passo de tempo)."""
    x = list(x)
    inclinacoes = []
    for i in range(len(x) - 1):
        for j in range(i + 1, len(x)):
            inclinacoes.append((x[j] - x[i]) / (j - i))
    return float(np.median(inclinacoes))


# ------------------------------------------------------------------------------------------------------------------
# Correlação com bootstrap em blocos
# ------------------------------------------------------------------------------------------------------------------
def correlacao(x, y, metodo="pearson"):
    """Coeficiente de correlação de Pearson ou de Spearman (pares com valor vazio são descartados)."""
    tab = pd.DataFrame({"x": x, "y": y}).dropna()
    if metodo == "spearman":
        return stats.spearmanr(tab["x"], tab["y"]).statistic
    return stats.pearsonr(tab["x"], tab["y"]).statistic


def bootstrap_blocos(x, y, bloco=3, n_reamostras=1000, metodo="pearson", semente=1):
    """Intervalo de 95% da correlação por bootstrap em blocos móveis.

    Em vez de sortear pares soltos (o que ignora a dependência entre meses vizinhos), sorteia PEDAÇOS seguidos de
    tamanho `bloco` e cola um atrás do outro até ter o tamanho da série. A correlação é recalculada em cada
    reamostra. Se o intervalo de 95% não contém o zero, a correlação é significativa a 5%.

    Devolve (r, limite inferior, limite superior, significativa).
    """
    tab = pd.DataFrame({"x": list(x), "y": list(y)}).dropna().reset_index(drop=True)
    n = len(tab)
    r = correlacao(tab["x"], tab["y"], metodo)
    xs = tab["x"].to_numpy()
    ys = tab["y"].to_numpy()
    if metodo == "spearman":                       # Spearman = Pearson calculado sobre os postos (ranks)
        xs = stats.rankdata(xs)
        ys = stats.rankdata(ys)
    gerador = np.random.default_rng(semente)
    inicios_possiveis = n - bloco + 1
    resultados = []
    for k in range(n_reamostras):
        posicoes = []
        while len(posicoes) < n:
            inicio = gerador.integers(0, inicios_possiveis)     # sorteia onde o bloco começa
            posicoes.extend(range(inicio, inicio + bloco))
        posicoes = posicoes[:n]
        resultados.append(np.corrcoef(xs[posicoes], ys[posicoes])[0, 1])   # correlação da reamostra
    baixo, alto = np.percentile(resultados, [2.5, 97.5])
    return r, baixo, alto, (baixo > 0) or (alto < 0)


# ------------------------------------------------------------------------------------------------------------------
# Contingência
# ------------------------------------------------------------------------------------------------------------------
def contingencia(fase, classe):
    """Tabela de contingência fase × classe, teste qui-quadrado, probabilidade condicional e risco relativo.

    Devolve um dicionário com:
      tabela   : contagem de meses em cada combinação;
      p_valor  : do teste qui-quadrado de independência;
      prob     : P(classe | fase), em %;
      clima    : P(classe) considerando todos os meses, em %;
      risco    : risco relativo = P(classe | fase) / P(classe).
    """
    tab = pd.crosstab(pd.Series(fase, name="fase"), pd.Series(classe, name="classe"))
    qui2 = stats.chi2_contingency(tab)
    prob = tab.div(tab.sum(axis=1), axis=0) * 100          # cada linha dividida pelo total da linha
    clima = tab.sum(axis=0) / tab.values.sum() * 100       # proporção de cada classe no total
    risco = prob / clima
    return {"tabela": tab, "p_valor": qui2.pvalue, "prob": prob.round(1), "clima": clima.round(1),
            "risco": risco.round(2)}


# ------------------------------------------------------------------------------------------------------------------
# Kruskal-Wallis e Dunn
# ------------------------------------------------------------------------------------------------------------------
def kruskal_dunn(valores, grupos):
    """Kruskal-Wallis entre os grupos e, em seguida, o teste de Dunn para cada par (com Bonferroni).

    Devolve (valor-p do Kruskal-Wallis, tabela de Dunn com o valor-p ajustado de cada par).
    """
    tab = pd.DataFrame({"v": list(valores), "g": list(grupos)}).dropna()
    nomes = sorted(tab["g"].unique())
    amostras = [tab.loc[tab["g"] == nome, "v"] for nome in nomes]
    p_kw = stats.kruskal(*amostras).pvalue

    tab["posto"] = tab["v"].rank()                 # postos (ranks) de todos os valores juntos
    n = len(tab)
    _, contagem_empates = np.unique(tab["v"], return_counts=True)
    correcao = np.sum(contagem_empates ** 3 - contagem_empates) / (12 * (n - 1))
    pares = []
    numero_de_pares = len(nomes) * (len(nomes) - 1) / 2
    for a in range(len(nomes)):
        for b in range(a + 1, len(nomes)):
            ga = tab[tab["g"] == nomes[a]]
            gb = tab[tab["g"] == nomes[b]]
            dif = ga["posto"].mean() - gb["posto"].mean()
            erro = np.sqrt((n * (n + 1) / 12 - correcao) * (1 / len(ga) + 1 / len(gb)))
            z = dif / erro
            p = 2 * (1 - stats.norm.cdf(abs(z)))
            pares.append({"grupo_1": nomes[a], "grupo_2": nomes[b], "z": round(z, 2),
                          "p_ajustado": min(p * numero_de_pares, 1.0)})
    return p_kw, pd.DataFrame(pares)
