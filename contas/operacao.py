class Operacao:
    def __init__(self, tipo, valor, origem, data):
        self.tipo = tipo
        self.valor = valor
        self.origem = origem
        self.data = data

    def __str__(self):
        return "{} R${:>10.2f}{:>15}".format(self.tipo, self.valor, self.origem)
