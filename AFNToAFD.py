from pprint import pprint

class AutomataNoDeterminista(object):
    def __init__(self, **kargs):
        self.estados = kargs['states']
        self.simbolosDeEntrada = kargs['input_symbols']
        self.transiciones = kargs['transitions']
        self.estadoInicial = kargs['initial_state']
        self.estadosFinales = kargs['final_states']

    def getEstados(self):
        return self.estados

    def getSimbolosDeEntrada(self):
        return self.simbolosDeEntrada

    def getTransiciones(self):
        return self.transiciones

    def getEstadoInicial(self):
        return self.estadoInicial

    def getEstadosFinales(self):
        return self.estadosFinales

    def getTransicion(self, estado):
        return self.transiciones[estado]

class CambiarDeAutomata(object):
    def __init__(self, automataNoDeterminista):
        self.automataNoDeterminista = automataNoDeterminista
        self.estadoInicial = self.getClausura(self.automataNoDeterminista.getEstadoInicial())
        self.estados = [self.estadoInicial]
        self.simbolosDeEntrada = self.automataNoDeterminista.getSimbolosDeEntrada()
        self.transiciones = {}
        self.estadosFinales = set()
        estadosSinRevisar = self.estados.copy()
        while estadosSinRevisar:
            estadoSinRevisar = estadosSinRevisar[0]
            transiciones = {}
            for simbolo in self.simbolosDeEntrada:
                transiciones[simbolo] = set()
                for estado in estadoSinRevisar:
                    transicion = self.automataNoDeterminista.getTransicion(estado)
                    if simbolo in transicion.keys():
                        for estadoEnTransicion in transicion[simbolo]:
                            transiciones[simbolo] |= self.getClausura(estadoEnTransicion)
                if transiciones[simbolo] not in self.estados:
                    self.estados.append(transiciones[simbolo])
                    estadosSinRevisar.append(transiciones[simbolo])
            self.transiciones[f'{estadoSinRevisar}'] = transiciones
            estadosSinRevisar.pop(0)
        for estado in self.estados:
            if any([estadoFinalInAutomata in estado for estadoFinalInAutomata in self.automataNoDeterminista.getEstadosFinales()]):
                self.estadosFinales |= estado
        # print(f'estados: {self.estados}')
        # print(f'simbolos de entrada: {self.simbolosDeEntrada}')
        # print('transiciones:')
        # pprint(self.transiciones)
        # print(f'estadoInicial: {self.estadoInicial}')
        # print(f'estados finales: {self.estadosFinales}')
        pprint(self.__dict__)

    def getClausura(self, estado):
        transiciones = self.automataNoDeterminista.getTransicion(estado)
        if '' not in transiciones.keys():
            return {estado}
        else:
            return {estado} | transiciones['']

if __name__ == '__main__':
    CambiarDeAutomata(AutomataNoDeterminista(
        states={'q0', 'q1', 'q2'},
        input_symbols={'0','1'},
        transitions={
            'q0': {'0': {'q0','q1'}, '1': {'q0'}},
            'q1': {'1': {'q2'}},
            'q2': {},
        },
        initial_state='q0',
        final_states={'q2'}
    ))
