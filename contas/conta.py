from abc import ABC, abstractmethod
from datetime import date, timedelta
from itertools import groupby

from helpers import auth_required
from operacao import Operacao


class Conta(ABC):
	def __init__(self, identificador, dono, senha):
		self.identificador = identificador
		self.dono = dono
		self.senha = senha
		self.superuser = False
		self.saldo = 0
		self.limite = 0
		self.juros = 0
		self.autenticado = False
		self.operacoes = []

	@abstractmethod
	def fechar(self):
		confirm = bool(int(input("Deseja mesmo encerrar a conta?")))
		if confirm:
			print("Conta encerrada! Sacados R${:.2f}".format(self.saldo))
			del self

	@abstractmethod
	def corrigir(self):
		self.saldo = self.saldo + self.saldo * self.juros

	def get_dono(self):
		return self.dono

	def depositar(self, valor, origem):
		if valor > 0:
			self.saldo += valor
			print("Despositados R${:.2f}".format(valor))
			self.registrar_operacao("+", valor, origem, date.today())

		else:
			raise ValueError("Só é possível depositar valores acima de R$0,00")

	def autenticar(self, senha):
		self.autenticado = self.senha == senha
		return self.autenticado

	def deslogar(self):
		self.autenticado = False

	@auth_required
	def set_senha(self, nova_senha):
		self.senha = nova_senha

	@auth_required	
	def sacar(self, valor, origem):
		if self.saldo - valor > self.limite:
			self.saldo - valor
			print("Sacados R${:.2f}".format(valor))
			self.registrar_operacao("-", valor, origem, date.today())
		else:
			raise ValueError("Não há limite suficiente na conta")

	@auth_required
	def tirar_extrato(self):
		data_limite = date.today() - timedelta(days=30)
		operacoes_para_extrato = filter(lambda x: x.data >= data_limite, self.operacoes)
		operacoes_para_extrato = sorted(operacoes_para_extrato, lambda x: (x.data, x.tipo))
		grouped = groupby(operacoes_para_extrato, lambda x: x.data)

		for data, operacoes in grouped:
			print(data.strftime("%d/%m/%Y"))
			for operacao in operacoes:
				print(operacao)

	@auth_required
	def verificar_saldo(self):
		return self.saldo

	def registrar_operacao(self, tipo, valor, origem, data):
		self.operacoes.append(Operacao(tipo, valor, origem data))

	def is_superuser(self):
		return self.superuser
