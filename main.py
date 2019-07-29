from banco import Banco
from atm import Atm
from contas import ContaPoupanca, ContaCorrente, ContaAdministrativa


def main():
    banco = Banco("BBF", "12312")
    conta_corrente = banco.abrir_conta(ContaCorrente, "Jorge", "12345", "123")
    conta_poupanca = banco.abrir_conta(ContaPoupanca, "José", "12345", "321")
    conta_gerente = banco.abrir_conta(ContaAdministrativa, "Maercelo", "12345", "777")
    atm = Atm(banco)

    while True:
        opcao = input("""
        XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
        XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
        XX                BANCO DA FAMÍLIA FELIZ                XX
        XX    Onde você, cliente, é nosso maior patrimônio!     XX
        XX                                                      XX
        XX  01. Atendimento Mesas                               XX
        XX  02. Autoatendimento                                 XX
        XX  X. Sair                                             XX
        XX                                                      XX
        XX                                                      XX
        XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
        """)

        while opcao not in ["01", "02", "X"]:
            opcao = input("Digite uma opcao válida")

        if opcao == "01":
            banco.iniciar_atendimento()

        elif opcao == "02":
            atm.iniciar_atendimento()

        else:
            return


if __name__ == '__main__':
    main()