class FilaTandem:

    def __init__(self, config) -> None:
        self.FILA1 = 0
        self.FILA2 = 0
        self.tempo = 0.0
        self.fila_1_arrival_limits = config['fila_1_arrival_limits']
        self.fila_1_serv_limits = config['fila_1_serv_limits']
        self.fila_2_serv_limits = config['fila_2_serv_limits']
        self.sementes = config['sementes']
        self.semente = 0
        self.fila_1_cap = config['fila_1_cap']
        self.fila_2_cap = config['fila_2_cap']
        self.fila_1_serv = config['fila_1_serv']
        self.fila_2_serv = config['fila_2_serv']

    def escalonador(self, tempo_inicial):
        self.escalonador_eventos = []
        self.tabela_estados_fila1 = []
        self.tabela_estados_fila2 = []
        # cria um vetor estado inicial com tamanho 3 + (capacidade + 1)
        fila_1_estado = [0.0] * (4 + (self.fila_1_cap + 1))
        fila_1_estado[0] = None
        fila_1_estado[1] = self.FILA1
        fila_1_estado[2] = self.FILA2
        fila_1_estado[3] = self.tempo
        self.tabela_estados_fila1.append(fila_1_estado)

        fila_2_estado = [0.0] * (4 + (self.fila_2_cap + 1))
        fila_2_estado[0] = None
        fila_2_estado[1] = self.FILA1
        fila_2_estado[2] = self.FILA2
        fila_2_estado[3] = self.tempo
        self.tabela_estados_fila2.append(fila_2_estado)

        # novo evento sem sorteio
        evento = ['CH1', tempo_inicial, 0.0]
        self.escalonador_eventos.append(evento)
        while self.semente < len(self.sementes):
            self.escalonador_eventos.sort( key=lambda x: x[1] )
            evento = self.escalonador_eventos.pop(0) 
            tempo_anterior = self.tempo
            self.tempo = evento[1]
            if evento[0] == 'CH1':
                if self.FILA1 < self.fila_1_cap:
                    self.FILA1 += 1
                    if self.FILA1 <= self.fila_1_serv:
                        self.agendaP12(self.tempo)
                self.agendaCH1(self.tempo)
            elif evento[0] == 'SA2':
                self.FILA2 -= 1
                if self.FILA2 > 0:
                    self.agendaSA2(self.tempo)
            elif evento[0] == 'P12':
                self.FILA1 -= 1
                if self.FILA1 >= self.fila_1_serv:
                    self.agendaP12(self.tempo)
                if self.FILA2 < self.fila_2_cap:
                    self.FILA2 += 1
                    if self.FILA2 <= self.fila_2_serv:
                        self.agendaSA2(self.tempo)       

            self.calculaEstado(evento, tempo_anterior)
        return self.tabela_estados_fila1[-1], self.tabela_estados_fila2[-1]

    def calculaEstado(self, evento, tempo_anterior):
        fila_1_ultimo_estado = self.tabela_estados_fila1[-1]
        fila_2_ultimo_estado = self.tabela_estados_fila2[-1]
        fila_1_ultima_fila = fila_1_ultimo_estado[1]
        fila_2_ultima_fila = fila_2_ultimo_estado[2]

        fila_1_novo_estado = fila_1_ultimo_estado.copy()
        fila_2_novo_estado = fila_2_ultimo_estado.copy()

        fila_1_novo_estado[0] = evento[0]
        fila_1_novo_estado[1] = self.FILA1
        fila_1_novo_estado[2] = self.FILA2
        fila_1_novo_estado[3] = self.tempo
        fila_2_novo_estado[0] = evento[0]
        fila_2_novo_estado[1] = self.FILA1
        fila_2_novo_estado[2] = self.FILA2
        fila_2_novo_estado[3] = self.tempo        
        # Calcula a diferença entre o tempo atual e o tempo anterior
        diferenca = self.tempo - tempo_anterior

        # Atualiza o tempo durante o qual a fila manteve a mesma quantidade de pessoas que tinha anteriormente
        # Soma a diferença de tempo ao tempo anterior durante o qual a fila permaneceu com a mesma quantidade de pessoas que tinha anteriormente
        fila_1_novo_estado[4 + fila_1_ultima_fila] = diferenca + fila_1_ultimo_estado[4 + fila_1_ultima_fila]
        fila_2_novo_estado[4 + fila_2_ultima_fila] = diferenca + fila_2_ultimo_estado[4 + fila_2_ultima_fila]

        self.tabela_estados_fila1.append(fila_1_novo_estado)
        self.tabela_estados_fila2.append(fila_2_novo_estado)

    def _sorteio(self, min_max):
        if self.semente == len(self.sementes):
            return 0
        self.semente += 1
        return (min_max[1] - min_max[0]) * self.sementes[self.semente - 1] + min_max[0]

    def agendaCH1(self, tempo):
        sorteio = self._sorteio(self.fila_1_arrival_limits)
        evento = ['CH1', tempo + sorteio, sorteio]
        self.escalonador_eventos.append(evento)

    def agendaSA2(self, tempo):
        sorteio = self._sorteio(self.fila_2_serv_limits)
        evento = ['SA2', tempo + sorteio, sorteio]
        self.escalonador_eventos.append(evento)

    def agendaP12(self, tempo):
        sorteio = self._sorteio(self.fila_1_serv_limits)
        evento = ['P12', tempo + sorteio, sorteio]
        self.escalonador_eventos.append(evento)