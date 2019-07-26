from contas import Conta
import random


def gerar_identificador():
    return "{}{}.{}{}{}-{}".format(*random.sample(range(1, 10), 6))


class Banco:
    nome = ""
    identificador = ""
    contas = {}

    def __init__(self, nome, identificador):
        self.nome = nome
        self.identificador = identificador
        self.contas = {}

    def get_contas(self):
        return self.contas.keys()

    def get_conta(self, identificador):
        return self.contas.get(identificador, None)

    def abrir_conta(self, tipo_conta, dono, senha, identificador=gerar_identificador()):
        while identificador in self.contas:
            identificador = gerar_identificador()

        if issubclass(tipo_conta, Conta):
            conta = tipo_conta(identificador, dono, senha)
            self.contas[identificador] = conta

            return conta

        else:
            raise TypeError("'tipo_conta' deve ser uma subclasse de 'Conta'")

    def encerrar_conta(self, identificador, senha):
        conta = self.get_conta(identificador)

        if conta.autenticar(senha):
            conta.fechar()
