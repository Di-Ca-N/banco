from datetime import date

from .conta import Conta
from helpers.decorators import auth_required


class ContaPoupanca(Conta):
    """
    Define conta com  comportamento de poupança
    """
    def __init__(self, identificador, dono, senha, criacao=date.today()):
        """Inicializa conta poupança"""
        super().__init__(identificador, dono, senha, criacao)
        self.juros = 0.005  # Juros padrão de 0,5%

    @auth_required
    def fechar(self):
        """
        Implementação do método abstrato fechar de Conta

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
        super().corrigir()
