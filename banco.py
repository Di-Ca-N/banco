from contas import Conta
import random


class Banco:
	nome = ""
	identificador = ""
	contas = {}

	def __init__(self, nome, identificador):
		self.nome = nome
		self.identificador = identificador

	def get_contas(self):
		return self.contas.keys()

	def get_conta(self, identificador):
		return self.contas.get(identificador, None)

	def abrir_conta(self, tipo_conta, dono, senha):
		identificador = self.gerar_identificador()

		while identificador in self.contas:
			identificador = self.gerar_identificador()

		if issubclass(tipo_conta, Conta):
			conta = tipo_conta(identificador, dono, senha)
			self.contas[identificador] = conta

			return conta

		else:
			raise TypeError("'tipo_conta' deve ser uma subclasse de 'Conta'")

	def gerar_identificador(self):
		return "{}{}.{}{}{}-{}".format(*random.sample(range(1, 10), 6))

	def encerrar_conta(self, identificador, senha):
		conta = self.get_conta(identificador)

		if conta.autenticar(senha):
			conta.fechar()
