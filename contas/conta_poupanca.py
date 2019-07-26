from .conta import Conta
from helpers import auth_required


class ContaPoupanca(Conta):
    def __init__(self, identificador, dono, senha):
        super().__init__(identificador, dono, senha)
        self.juros = 0.5

    @auth_required
    def fechar(self):
        confirm = bool(int(input("Deseja mesmo encerrar a conta?")))
        if confirm:
            print("Conta encerrada! Sacados R${:.2f}".format(self.__saldo))
            del self

    def corrigir(self):
        super().corrigir()
