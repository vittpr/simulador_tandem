from FilaTandem import FilaTandem
from utils import calcResultados, criaSementes, escreveresult1, escreveresult2


config = {
        'fila_1_arrival_limits':[1,4], # Chegadas entre 1 e 4 para a fila 1
        'fila_1_serv_limits':[3,4], # Atendimentos entre 3 e 4 para a fila 1
        'fila_2_serv_limits':[2,3], # Atendimentos entre 2 e 3 para a fila 2
        'sementes':[], # Sementes vazias para serem preenchidas após a execução
        'fila_1_serv':2,
        'fila_1_cap':3,
        'fila_2_serv':1,
        'fila_2_cap':5
}

sementes = [0.9921, 0.0004, 0.5534, 0.2761, 0.3398]

fila_1_simu = []
fila_2_simu = []
for semente in sementes:
    sementes = criaSementes(semente, 100000)
    config['sementes'] = sementes
    filaTandem = FilaTandem(config)
    estados1, estados2 = filaTandem.escalonador(2.5000)
    fila_1_simu.append(estados1[3:])
    fila_2_simu.append(estados2[3:])

result1 = calcResultados(fila_1_simu, config['fila_1_cap'])
result2 = calcResultados(fila_2_simu, config['fila_2_cap'])

escreveresult2([fila_1_simu, fila_2_simu], 'resultados_por_estados.txt')
escreveresult1([result1, result2], 'resultados.txt')