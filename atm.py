from banco import Banco
from datetime import datetime

class Atm:
	dinheiro = {}
	historico = []
	conta_autenticada = None
	banco = None

	def __init__(self, banco):
		self.dinheiro = {}
		self.historico = []
		self.conta_autenticada = None
		self.banco = banco

	def iniciarATM(self):
		loop = True
		while loop:
			if self.conta_autenticada is None:
				self.atender_pessoa()
			else:
				print(self.conta_autenticada)
				if self.conta_autenticada.is_superuser():
					self.atender_gerente()
				else:
					self.atender_cliente()


	def atender_pessoa(self):
		alternativa = input("""
		XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
		XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
		XX                BANCO DA FAMÍLIA FELIZ                XX
		XX    Onde você, cliente, é nosso maior patrimônio!     XX
		XX                                                      XX
		XX  01. Entrar na conta                                 XX
		XX  02. Realizar Depósito                               XX
		XX  X. Sair                                             XX
		XX                                                      XX
		XX                                                      XX
		XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
		""")
		if alternativa == "01":
			identificador = input("Identificador da conta: ")
			senha = input("Senha: ")
			self.conectar_conta(identificador, senha)

		elif alternativa == "02":
			tipo = "DEPÓSITO"
			conta_origem = input("Doador: ")
			conta_destino = self.banco.get_conta(input("Conta destino: "))
			valor = float(input("Valor: "))
			self.deposito(conta_destino, valor)
			self.gravar_historico(tipo, valor, conta_origem, conta_destino, datetime.now())

		elif alternativa == "X":
			loop = False


	def atender_gerente(self):
		alternativa = input("""
		XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
		XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
		XX                BANCO DA FAMÍLIA FELIZ                XX
		XX             Trabalhe, escravo, trabalhe!             XX
		XX                                                      XX
		XX  01. Saldar ATM                                      XX
		XX  02. Resetar ATM                                     XX
		XX  03. Listar operações recentes                       XX
		XX  04. Depositar na ATM                                XX
		XX  X. 	Desconectar                                     XX
		XX                                                      XX
		XX                                                      XX
		XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
		""")
		if alternativa == "01":
			self.listar_notas()

		elif alternativa == "02":
			lavagemdedinheiro = input("Você tem absoluta certeza do que está fazendo? S/N")
			if lavagemdedinheiro == "S" or lavagemdedinheiro == "s":
				self.reset()

		elif alternativa == "03":
			self.mostrar_historico()

		elif alternativa == "04":
			pergunta = "S"
			tipo, destino = "DEPOSITO", "ATM"
			while pergunta == "S":
				nota = input("Qual o valor da nota selecionada? \n")
				qntd = input("Quantas notas? \n")
				self.adicionar_dinheiro(nota, qntd)
				self.gravar_historico(tipo, valor, destino, datetime.now())
				pergunta = input("Você ainda quer depositar mais dinheiro? S/N \n")

		elif alternativa == "X":
			self.desconectar_conta()


	def atender_cliente(self):
		alternativa = input("""
		XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
		XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
		XX                BANCO DA FAMÍLIA FELIZ                XX
		XX      Sua felicidade é nossa maior prioridade!        XX
		XX                                                      XX
		XX  01. Sacar dinheiro                                  XX
		XX  02. Depositar dinheiro                              XX
		XX  03. Transferir dinheiro                             XX
		XX  04. Extrato da conta                                XX
		XX  05. Saldo da conta                                  XX
		XX  X. 	Desconectar                                     XX
		XX                                                      XX
		XX                                                      XX
		XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

		""")

		if alternativa == "01":
			tipo = "SAQUE"
			valor = float(input("Valor solicitado:"))
			if self.saque(self.conta_autenticada, valor):
				self.gravar_historico(tipo, valor, self.conta_autenticada, None, datetime.now())
			else:
				print("Ocorreu um problema durante a transação. Cheque as informações solicitadas e o saldo da conta.")

		elif alternativa == "02":
			tipo = "DEPÓSITO"

			valor = float(input("Valor: "))
			if self.deposito(self.conta_autenticada, valor):
				self.gravar_historico(tipo, valor, self.conta_autenticada, None, datetime.now())
			else:
				print("O valor a ser depositado é inválido.")

		elif alternativa == "03":
			tipo = "TRANSFERÊNCIA"
			conta_destino = input("Conta destino: ")
			if get_conta(conta_destino) is not None:
				valor = input("Valor a transferir:")
				if self.saque(self.conta_autenticada, valor) and self.deposito(conta_destino, valor):
					self.gravar_historico(tipo, valor, self.conta_autenticada, conta_destino, datetime.now())
				else:
					print("A transferência do valor solicitado não pôde ser concluída. Verifique suas informações, parça.")
		elif alternativa == "04":
			print(self.fornecer_extrato(self.conta_autenticada))

		elif alternativa == "05":
			print("seu saldo é", self.fornecer_saldo(self.conta_autenticada))

		elif alternativa == "X":
			self.desconectar_conta()
			
	def listar_notas(self):
		relatorio_notas = ""
		for nota, quantidade in dinheiro:
			relatorio_notas += "Valor: R${} | Quantidade: {} \n".format(nota, quantidade)

	def mostrar_historico(self):
		for evento in self.historico:
			print(evento)

	def gravar_historico(self, tipo, valor, conta_origem, conta_destino, data):
		evento = "OPERAÇÃO: {} | VALOR: R$ {} | CONTA DE ORIGEM: {} | CONTA DESTINO: {} | DATA: {}".format(tipo, valor, conta_origem, conta_destino, data)
		self.historico.append(evento)

	def adicionar_dinheiro(self, nota, qtd):
		self.dinheiro[nota] += qtd

	def reset(self):
		self.dinheiro = {}
		self.historico = []

	def conectar_conta(self, identificador, senha):
		conta = self.banco.get_conta(identificador)
		if conta.autenticar(senha):
			self.conta_autenticada = conta
		else:
			print("Sua senha não foi aceita. Por favor, confira os dados informados.")

	def desconectar_conta(self):
		self.conta_autenticada.deslogar()
		self.conta_autenticada = None
		print("Você não está mais conectado.")

	def saque(self, conta_origem, valor):
		try:
			conta_origem.debitar(valor, str(conta_origem))
			return True

		except ValueError as erro:
			print(erro.args[0])
			return False

	def deposito(self, conta_destino, valor):
		try: 
			conta_destino.creditar(valor, str(conta_destino))
			return True

		except ValueError as erro:
			print(erro.args[0])
			return False

	def fornecer_extrato(self, conta_origem):
		extrato_conta = conta_origem.get_extrato()
		return extrato_conta

	def fornecer_saldo(self, conta_origem):
		saldo_conta = conta_origem.get_saldo()
		return saldo_conta
