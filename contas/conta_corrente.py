from conta import Conta
from helpers import auth_required


class ContaCorrente(Conta):
	@auth_required
	def fechar(self):
		if self.saldo < 0:
			print("Você precisa quitar o débito de R${:.2f} para encerrar a conta".format(-self.saldo))

		else:
			confirm = bool(int(input("Deseja mesmo encerrar a conta?")))
			if confirm:
				print("Conta encerrada! Sacados R${:.2f}".format(self.saldo))
				del self


	def set_limite(self, limite):
		self.limite = limite

	def corrigir(self):
		if self.saldo < 0:
			super().corrigir()
