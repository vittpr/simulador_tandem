import numpy as np
from tabulate import tabulate

def calcResultados(lista, capacidade):

    np.set_printoptions(precision=4, suppress=True)
    data_array = np.array(lista)
    column_means = np.mean(data_array, axis=0)

    resultados = []
    for i in range(capacidade + 1):
        resultado = [i, column_means[i + 1], (column_means[i + 1] / column_means[0]) * 100]
        resultados.append(resultado)
    resultados.append(['TOTAL', column_means[0], 100])
    return resultados

def criaSementes(semente, n):
    sementes = []
    for i in range(n):
        sementes.append(semente)
        semente = (semente * 5) % 1
    return sementes

def calcResultAux(lista, capacidade):
    resultados = []
    for i in range(capacidade + 1):
        resultado = [i, lista[-1][i + 1], (lista[-1][i + 1] / lista[-1][0]) * 100]
        resultados.append(resultado)
    resultados.append(['TOTAL', lista[-1][0], 100])
    return resultados

def escreveresult1(resultados, nome_arquivo):
    with open(nome_arquivo, 'w') as arquivo:
        for i, resultado in enumerate(resultados):
            arquivo.write('Fila ' + str(i + 1) + '\n')
            arquivo.write(tabulate(resultado, headers=['Estado', 'Tempo acumulado', 'Probabilidade (%)']) + '\n\n')

def escreveresult2(resultados, nome_arquivo):
    with open(nome_arquivo, 'w') as arquivo:
        for i, resultado in enumerate(resultados):
            arquivo.write('Fila ' + str(i + 1) + '\n')
            arquivo.write(str(tabulate(resultado)) + '\n')
        arquivo.write('\n')