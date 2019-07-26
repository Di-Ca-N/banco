from banco import Banco
from contas import ContaCorrente, ContaPoupanca, ContaSuper
from atm import Atm

banco = Banco("BBF", "12312")
banco.abrir_conta(ContaCorrente, "João", "12345", "123")
banco.abrir_conta(ContaSuper, "Pedro", "12345", "1343")
atm = Atm(banco)

atm.iniciarATM()
