from datetime import date

from .conta import Conta
from helpers.decorators import auth_required


class ContaAdministrativa(Conta):
    def __init__(self, identificador, dono, senha, criacao=date.today()):
        super().__init__(identificador, dono, senha, criacao)
        self.superuser = True

    @auth_required
    def fechar(self):
        confirm = bool(int(input("Deseja mesmo encerrar a conta?")))
        if confirm:
            print("Conta encerrada!".format(self.saldo))
            del self

    def corrigir(self):
        print("Não é possível corrigir o valor de uma conta administrativa")

    def creditar(self, valor, origem, data=date.today()):
        print("Não é possível depositar em uma conta administrativa")

    @auth_required
    def debitar(self):
        print("Não é possível sacar de uma conta administrativa")
