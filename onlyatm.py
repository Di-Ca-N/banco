from atm import Atm
from banco import Banco
from contas import ContaCorrente, ContaAdministrativa, ContaPoupanca

banco = Banco("", "")
conta_corrente = banco.abrir_conta(ContaCorrente, "Jorge", "12345", "123")
conta_poupanca = banco.abrir_conta(ContaPoupanca, "José", "12345", "321")
conta_gerente = banco.abrir_conta(ContaAdministrativa, "Maercelo", "12345", "777")

a = Atm(banco)
a.iniciar_atendimento()
