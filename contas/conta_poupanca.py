from datetime import date

from .conta import Conta
from helpers.decorators import auth_required


class ContaPoupanca(Conta):
    def __init__(self, identificador, dono, senha, criacao=date.today()):
        super().__init__(identificador, dono, senha, criacao)
        self.juros = 0.5

    @auth_required
    def fechar(self):
        confirm = bool(int(input("Deseja mesmo encerrar a conta?")))
        if confirm:
            print("Conta encerrada! Sacados R${:.2f}".format(self.saldo))
            del self

    def corrigir(self):
        super().corrigir()
