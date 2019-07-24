from abc import ABC, abstractmethod
from helpers import auth_required


class Conta(ABC):
	def __init__(self, identificador, dono, senha, superuser=False):
		self.identificador = identificador
		self.dono = dono
		self.senha = senha
		self.superuser = superuser
		self.saldo = 0
		self.limite = 0
		self.juros = 0
		self.autenticado = False
		self.operacoes = []

	@abstractmethod
	def fechar(self):
		raise NotImplementedError()

	@abstractmethod
	def corrigir(self):
		self.saldo = self.saldo + self.saldo * self.juros

	def set_juros(self, taxa):
		self.juros = taxa

	def get_dono(self):
		return self.dono

	def depositar(self, valor, tipo_operacao="+"):
		if valor > 0:
			self.saldo += valor

		else:
			raise ValueError("Só é possível depositar valores acima de 0")

	def autenticar(self, senha):
		self.autenticado = self.senha == senha
		return self.autenticado

	def deslogar(self):
		self.autenticado = False

	@auth_required
	def set_senha(self, nova_senha):
		self.senha = nova_senha

	@auth_required	
	def sacar(self, valor):
		if self.saldo - valor > self.limite:
			self.saldo - valor
		else:
			raise ValueError("Não há limite suficiente na conta")

	@auth_required
	def tirar_extrato(self):
		return self.operacoes


	@auth_required
	def verificar_saldo(self):
		return self.saldo

	def registrar_operacao(self, tipo, valor, data):
		self.operacoes.append((tipo, valor, data))
