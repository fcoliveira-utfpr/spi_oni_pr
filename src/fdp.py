"""Funções de distribuição de probabilidade (FDP) usadas no cálculo do SPI.

As quatro distribuições do trabalho: Gama, Gumbel, Log-Normal e Exponencial.
Todas são ajustadas por máxima verossimilhança com a biblioteca scipy.

Como a chuva acumulada pode ter valores iguais a zero (raro no Paraná, mas acontece em alguns trimestres de inverno
no norte do estado), a distribuição é ajustada só aos valores positivos, e a probabilidade de zero (q) é tratada à
parte (distribuição mista; Guttman, 1999):

    H(x) = q + (1 - q) * G(x)
"""
import numpy as np
from scipy import stats

# nome usado no trabalho -> distribuição da scipy
DISTRIBUICOES = {
    "Gama": stats.gamma,
    "Gumbel": stats.gumbel_r,
    "Log-Normal": stats.lognorm,
    "Exponencial": stats.expon,
}

# distribuições que começam em zero (o parâmetro de posição "loc" fica fixo em 0)
COMECA_EM_ZERO = ["Gama", "Log-Normal", "Exponencial"]

# número de parâmetros estimados de cada distribuição (usado no AIC)
N_PARAMETROS = {"Gama": 2, "Gumbel": 2, "Log-Normal": 2, "Exponencial": 1}


def so_positivos(valores):
    """Tira os valores vazios (NaN) e os zeros. Devolve um array do numpy."""
    valores = np.asarray(valores, dtype=float)
    valores = valores[~np.isnan(valores)]      # ~ quer dizer "não": fica com os que NÃO são NaN
    return valores[valores > 0]


def ajustar(valores, nome):
    """Ajusta a distribuição `nome` aos valores positivos. Devolve os parâmetros (tupla da scipy)."""
    x = so_positivos(valores)
    dist = DISTRIBUICOES[nome]
    if nome in COMECA_EM_ZERO:
        return dist.fit(x, floc=0)             # floc=0: a curva começa em zero
    return dist.fit(x)


def prob_zero(valores):
    """Proporção de valores iguais a zero (q), sem contar os vazios."""
    valores = np.asarray(valores, dtype=float)
    valores = valores[~np.isnan(valores)]
    if len(valores) == 0:
        return np.nan
    return np.mean(valores == 0)


def prob_acumulada(x, nome, parametros, q=0.0):
    """Probabilidade de a chuva acumulada ser menor ou igual a x: H(x) = q + (1 - q) G(x)."""
    dist = DISTRIBUICOES[nome]
    g = dist.cdf(x, *parametros)               # G(x): probabilidade pela distribuição ajustada
    return q + (1 - q) * g


def aic(valores, nome, parametros):
    """Critério de informação de Akaike: AIC = 2k - 2 ln(L). Quanto menor, melhor o ajuste."""
    x = so_positivos(valores)
    dist = DISTRIBUICOES[nome]
    log_verossimilhanca = np.sum(dist.logpdf(x, *parametros))
    return 2 * N_PARAMETROS[nome] - 2 * log_verossimilhanca


def teste_ks(valores, nome, parametros):
    """Teste de Kolmogorov-Smirnov clássico: devolve o valor-p.

    Atenção: com os parâmetros estimados dos próprios dados, o valor-p clássico fica alto demais (o teste "aprova"
    com facilidade). A versão corrigida, por simulação, é `testes_monte_carlo`.
    """
    x = so_positivos(valores)
    return stats.kstest(x, DISTRIBUICOES[nome].cdf, args=parametros).pvalue


def testes_monte_carlo(valores, nome, n_simulacoes=99, semente=1):
    """Valores-p dos testes de Kolmogorov-Smirnov (KS) e Anderson-Darling (AD) corrigidos por simulação.

    A scipy sorteia `n_simulacoes` amostras da distribuição ajustada, reajusta os parâmetros em cada uma e vê com que
    frequência a estatística do teste fica maior que a dos dados reais (princípio de Lilliefors, 1967).
    É lento: use nas estações em destaque.
    """
    x = so_positivos(valores)
    dist = DISTRIBUICOES[nome]
    conhecidos = {"loc": 0} if nome in COMECA_EM_ZERO else None
    resultado = {}
    for estatistica in ["ks", "ad"]:
        r = stats.goodness_of_fit(dist, x, known_params=conhecidos, statistic=estatistica,
                                  n_mc_samples=n_simulacoes, random_state=semente)
        resultado[estatistica] = r.pvalue
    return resultado
