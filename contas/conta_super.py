from .conta import Conta
from helpers import auth_required
from datetime import date


class ContaSuper(Conta):
    def __init__(self, identificador, dono, senha):
        super().__init__(identificador, "Gerência", senha)
        self._superuser = True

    @auth_required
    def fechar(self):
        confirm = bool(int(input("Deseja mesmo encerrar a conta?")))
        if confirm:
            print("Conta encerrada!".format(self.__saldo))
            del self

    def corrigir(self):
        pass

    def creditar(self, valor, origem, data=date.today()):
        raise ValueError("Não é possível depositar em uma conta administrativa!")

    @auth_required
    def debitar(self):
        raise ValueError("Não é possível sacar de uma conta administrativa!")
