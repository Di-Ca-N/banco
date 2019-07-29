from datetime import date

from .conta import Conta
from helpers.decorators import auth_required


class ContaCorrente(Conta):
    def __init__(self, identificador, dono, senha, criacao=date.today()):
        super().__init__(identificador, dono, senha, criacao)
        self.ask_limit()
        self.ask_juros()

    def ask_limit(self):
        sucess = False
        while not sucess:
            try:
                self.limite = -float(input("Limite da conta: R$"))
            except ValueError:
                print("Digite um limite válido")
            else:
                sucess = True

    def ask_juros(self):
        sucess = False
        while not sucess:
            try:
                self.juros = float(input("Juros da conta (%): ")) / 100
            except ValueError:
                print("Digite um juro válido")
            else:
                sucess = True

    @auth_required
    def fechar(self):
        if self.get_saldo() < 0:
            print("Você precisa quitar o débito de R${:.2f} para encerrar a conta".format(-self.saldo))

        else:
            super().fechar()

    def set_juros(self, taxa):
        self.juros = taxa

    def set_limite(self, limite):
        self.limite = -limite

    def corrigir(self):
        if self.saldo < 0:
            super().corrigir()
