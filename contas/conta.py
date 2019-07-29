from abc import ABC, abstractmethod
from datetime import date, timedelta
from itertools import groupby

from helpers.decorators import auth_required
from operacao import Operacao


class Conta(ABC):
    identificador = ""
    dono = None
    senha = ""
    saldo = 0.0
    limite = 0.0
    juros = 0.0
    autenticado = 0.0
    operacoes = []
    criacao = date.today()

    def __init__(self, identificador, dono, senha, criacao):
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

    def __str__(self):
        return str(self.dono)

    @abstractmethod
    def fechar(self):
        confirm = input("Deseja mesmo encerrar a conta?(S/N)").upper()
        if confirm == "S":
            print("Conta encerrada! Sacados R${:.2f}".format(self.saldo))
            return True
        return False

    @abstractmethod
    def corrigir(self):
        self.saldo = self.saldo + self.saldo * self.juros

    def get_dono(self):
        return self.dono

    def creditar(self, valor, origem, data=date.today()):
        if valor > 0:
            self.saldo += valor
            print("Despositados R${:.2f}".format(valor))
            self.registrar_operacao("+", valor, origem, data)

        else:
            raise ValueError("Só é possível depositar valores acima de R$0,00")

    def autenticar(self, senha):
        if self.senha == senha:
            self.autenticado = True
        return self.autenticado

    def deslogar(self):
        self.autenticado = False

    @auth_required
    def set_senha(self, nova_senha):
        self.senha = nova_senha

    @auth_required  
    def debitar(self, valor, origem, data=date.today()):
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
    def get_saldo(self) -> float:
        return self.saldo

    def registrar_operacao(self, tipo, valor, origem, data):
        self.operacoes.append(Operacao(tipo, valor, origem, data))

    def is_superuser(self):
        return self.superuser

    def is_autenticado(self):
        return self.autenticado
