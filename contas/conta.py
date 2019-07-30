from abc import ABC, abstractmethod
from datetime import date, timedelta
from itertools import groupby

from helpers.decorators import auth_required
from contas.operacao import Operacao


class Conta(ABC):
    """
    Classe asbtrata primitiva para a criação de contas

    Attributes:
        identificador: Identificador único
        dono: Objeto Pessoa
        senha: Senha de acesso à conta
        limite: Valor mínimo para o saldo
        juros: Taxa de juros utilizada para a correção dos valores da conta
        autenticado: Define se a conta está autenticada em alguma ATM, para autorizar ou negar
                     a execução de certas operações
        operacoes: Lista de objetos Operacao, que descrevem as operações efetuadas
        criacao: Data de criação da conta
        ultima_correcao: data em que o valor da conta foi corrigido pela última vez.
    """

    def __init__(self, identificador, dono, senha, criacao):
        """
        Inicializa uma conta

        Args:
            identificador: identificador único
            dono: objeto Pessoa
            senha: senha de acesso à conta
            criacao: data de criação da conta
        """
        self.identificador = identificador
        self.dono = dono
        self.criacao = criacao
        self.senha = senha
        self.superuser = False
        self.limite = 0
        self.juros = 0
        self.saldo = 0
        self.autenticado = False
        self.operacoes = []
        self.ultima_correcao = date.today()

    def __str__(self):
        return str(self.dono)

    @abstractmethod
    def fechar(self):
        """
        Método abstrato que gerencia o fechamento de contas. Contém implementação padrão

        Returns:
            True, se foi possível deletar a conta. False caso contrário
        """
        confirm = input("Deseja mesmo encerrar a conta?(S/N)").upper()
        if confirm == "S":
            print("Conta encerrada! Sacados R${:.2f}".format(self.saldo))
            return True
        return False

    @abstractmethod
    def corrigir(self):
        """
        Método abstrato para corrigir o valor na conta. Contém implementação padrão

        Returns:
            None
        """
        self.saldo = self.saldo + self.saldo * self.juros
        self.ultima_correcao = date.today()

    def creditar(self, valor, origem, data=date.today()):
        """
        Credita o valor informado na conta

        Args:
            valor: Valor a ser creditado. Deve ser um float maior que 0.
            origem: Origem do crédito, para ser mostrada no extrato
            data: Data do crédito

        Returns:
            None
        """
        if valor > 0:
            self.saldo += valor
            print("Despositados R${:.2f}".format(valor))
            self.registrar_operacao("+", valor, origem, data)

        else:
            raise ValueError("Só é possível depositar valores acima de R$0,00")

    def autenticar(self, senha):
        """
        Autentica a conta utilzizando a senha informada

        Args:
            senha: senha para tentar autenticação

        Returns:
            True, se a senha estiver correta. False, caso contrário
        """
        if self.senha == senha:
            self.autenticado = True
        return self.autenticado

    def deslogar(self):
        """
        Desloga a conta

        Returns:
            None
        """
        self.autenticado = False

    @auth_required
    def set_senha(self, nova_senha):
        """
        Autoriza a mudança de senha da conta. Requer autenticação
        Args:
            nova_senha:

        Returns:
            None
        """
        self.senha = nova_senha

    @auth_required  
    def debitar(self, valor, origem, data=date.today()):
        """
        Debita o valor informado da conta. requer autenticação
        Args:
            valor: Valor a ser debitado. Deve ser um float maior que 0
            origem: Origem do débito para extrato
            data: data do débito

        Returns:
            None
        """
        if valor > 0:
            if self.saldo - valor >= self.limite:
                self.saldo = self.saldo - valor
                print("Sacados R${:.2f}".format(valor))
                self.registrar_operacao("-", valor, origem, data)
                return True

            else:
                raise ValueError("Você não tem limite suficiente")

        else:
            raise ValueError("Não é possível sacar valor negativo")

    @auth_required
    def get_extrato(self, dias=30):
        """
        Emite o extrato da conta no período de tempo informado

        Args:
            dias: Quantidade de dias passados ao qual o extrato irá se referir

        Returns:
            Extrato como string
        """
        data_limite = date.today() - timedelta(days=dias)
        operacoes_para_extrato = filter(lambda x: x.data >= data_limite, self.operacoes)
        operacoes_para_extrato = sorted(operacoes_para_extrato, key=lambda x: (x.data, x.tipo))
        grouped = groupby(operacoes_para_extrato, lambda x: x.data)

        extrato = ""
        for data, operacoes in grouped:
            extrato += data.strftime("%d/%m/%Y") + "\n"
            for operacao in operacoes:
                extrato += str(operacao) + "\n"

        return extrato

    @auth_required
    def get_saldo(self):
        """
        Retorna o saldo da conta. Requer autenticação

        Returns:
            Saldo (float)
        """
        return self.saldo

    def registrar_operacao(self, tipo, valor, origem, data):
        """
        Registra operação no histórico da conta, para ser mostrada no extrato

        Args:
            tipo: Crédito ("+") ou débito ("-")
            valor: Valor da operação
            origem: Origem da operação
            data: Data de realização da operação

        Returns:
            None
        """
        self.operacoes.append(Operacao(tipo, valor, origem, data))
