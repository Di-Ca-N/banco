from .conta import Conta
from helpers import auth_required


class ContaCorrente(Conta):
    @auth_required
    def fechar(self):
        if self.__saldo < 0:
            print("Você precisa quitar o débito de R${:.2f} para encerrar a conta".format(-self.__saldo))

        else:
            super().fechar()

    def set_juros(self, taxa):
        self.juros = taxa

    def set_limite(self, limite):
        self.limite = limite

    def corrigir(self):
        if self.__saldo < 0:
            super().corrigir()
