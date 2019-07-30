from datetime import date

from .conta import Conta
from helpers.decorators import auth_required


class ContaCorrente(Conta):
    """
    Define conta com comportamento de conta corrente
    """
    def __init__(self, identificador, dono, senha, criacao=date.today(), limite=None, juros=None):
        """
            Inicializa conta corrente
        Args:
            identificador: identificador único
            dono: objeto Pessoa
            senha: senha de acesso à conta
            criacao: data de criação da conta
            limite: valor mínimo do saldo
            juros: taxa de juros
        """
        super().__init__(identificador, dono, senha, criacao)
        self.limite = -limite if limite is not None else self._ask_limit()
        self.juros = juros if juros is not None else self._ask_juros()

    def _ask_limit(self):
        sucess = False
        while not sucess:
            try:
                self.limite = -float(input("Limite da conta: R$"))
            except ValueError:
                print("Digite um limite válido")
            else:
                sucess = True

    def _ask_juros(self):
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
        """
        Implementação do método abstrato fechar da class Conta

        Returns:
            None
        """
        if self.get_saldo() < 0:
            print("Você precisa quitar o débito de R${:.2f} para encerrar a conta".format(-self.saldo))
            return False

        else:
            return super().fechar()

    def set_limite(self, limite):
        """
        Define limite para a conta

        Args:
            limite: novo saldo mínimo para a conta

        Returns:
            None
        """
        self.limite = -limite

    def corrigir(self):
        """
        Implementação do método abstrato corrigir da class Conta

        Returns:
            None
        """
        if self.saldo < 0:
            super().corrigir()
