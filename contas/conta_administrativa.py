from datetime import date

from .conta import Conta
from helpers.decorators import auth_required


class ContaAdministrativa(Conta):
    """
    Conta com privilégios administrativos
    """
    def __init__(self, identificador, dono, senha, criacao=date.today()):
        """
        Inicializa objeto ContaAdministrativa

        Args:
            identificador: identificador da conta
            dono: objeto Pessoa
            senha: senha de acesso
            criacao: data de criação
        """
        super().__init__(identificador, dono, senha, criacao)
        self.superuser = True  # Define a conta como superuser

    @auth_required
    def fechar(self):
        """
        Implementação do método abstrato "fechar" de Conta

        Returns:
            None
        """
        return super().fechar()

    def corrigir(self):
        """
        Implementação do método abstrato corrigir de Conta

        Returns:
            None
        """
        print("Não é possível corrigir o valor de uma conta administrativa")

    def creditar(self, valor, origem, data=date.today()):
        """
        Sobrescrita do método creditar de Conta

        Args:
            Não relevantes para essa implementação

        Returns:
            None
        """
        print("Não é possível depositar em uma conta administrativa")

    @auth_required
    def debitar(self, valor, origem, data=date.today()):
        """
        Sobrescrita do método debitar de Conta

        Args:
            Não relevantes para essa implementação

        Returns:
            None
        """
        print("Não é possível sacar de uma conta administrativa")
