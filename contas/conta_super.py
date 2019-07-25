from conta import Conta
from helpers import auth_required


class ContaSuper(Conta):
	def __init__(self, identificador, senha):
		super().__init__(identificador, None, senha)
		self.superuser = True

	@auth_required
	def fechar(self):
		confirm = bool(int(input("Deseja mesmo encerrar a conta?")))
		if confirm:
			print("Conta encerrada!".format(self.saldo))
			del self

	def corrige(self):
		pass

	def depositar(self):
		raise ValueError("Não é possível depositar em uma conta administrativa!")

	@auth_required
	def sacar(self):
		raise ValueError("Não é possível sacar de uma conta administrativa!")
