from abc import ABC, abstractmethod
from datetime import date, timedelta
from itertools import groupby

from helpers import auth_required
from operacao import Operacao


class Conta(ABC):
    def __init__(self, identificador, dono, senha):
        self.identificador = identificador
        self.dono = dono
        self.__senha = senha
        self.__superuser = False
        self.__saldo = 0
        self.__limite = 0
        self.__juros = 0
        self.__autenticado = False
        self.__operacoes = []

    def __str__(self):
        return "Conta {}".format(self.identificador)

    @abstractmethod
    def fechar(self):
        confirm = bool(int(input("Deseja mesmo encerrar a conta?")))
        if confirm:
            print("Conta encerrada! Sacados R${:.2f}".format(self.__saldo))
            del self

    @abstractmethod
    def corrigir(self):
        self.__saldo = self.__saldo + self.__saldo * self.__juros

    def get_dono(self):
        return self.dono

    def creditar(self, valor, origem):
        if valor > 0:
            self.__saldo += valor
            print("Despositados R${:.2f}".format(valor))
            self.registrar_operacao("+", valor, origem, date.today())

        else:
            raise ValueError("Só é possível depositar valores acima de R$0,00")

    def autenticar(self, senha):
        if self.__senha == senha:
            self.__autenticado = True
        return self.__autenticado

    def deslogar(self):
        self.__autenticado = False

    @auth_required
    def set_senha(self, nova_senha):
        self.__senha = nova_senha

    @auth_required  
    def debitar(self, valor, origem):
        if self.__saldo - valor > self.__limite:
            self.__saldo = self.__saldo - valor
            print("Sacados R${:.2f}".format(valor))
            self.registrar_operacao("-", valor, origem, date.today())
        else:
            print("Você não tem limite suficiente")

    @auth_required
    def tirar_extrato(self):
        data_limite = date.today() - timedelta(days=30)
        operacoes_para_extrato = filter(lambda x: x.data >= data_limite, self.__operacoes)
        operacoes_para_extrato = sorted(operacoes_para_extrato, key=lambda x: (x.data, x.tipo))
        grouped = groupby(operacoes_para_extrato, lambda x: x.data)

        extrato = ""
        for data, operacoes in grouped:
            extrato += data.strftime("%d/%m/%Y") + "\n"
            for operacao in operacoes:
                extrato += str(operacao) + "\n"

        return extrato

    @auth_required
    def verificar_saldo(self) -> float:
        return self.__saldo

    def registrar_operacao(self, tipo, valor, origem, data):
        self.__operacoes.append(Operacao(tipo, valor, origem, data))

    def is_superuser(self):
        return self.__superuser

    def is_autenticado(self):
        return self.__autenticado
