from banco import Banco
from atm import ATM
from contas import ContaPoupanca, ContaCorrente, ContaAdministrativa
from helpers.interface import Interface


def main():
    banco = Banco("BBF", "12312")
    banco.abrir_conta(ContaCorrente, "Jorge", "12345", "123", juros=0.1, limite=2000)
    banco.abrir_conta(ContaPoupanca, "José", "12345", "321")
    banco.abrir_conta(ContaAdministrativa, "Maercelo", "12345", "777")
    atm = ATM(banco)

    interface = Interface(
        title="BANCO DA FAMÍLIA FELIZ",
        message="Seja bem-vinda, potencial fonte de renda!",
        box_weight=2,
        bottom_weight=1,
        bottom_padding=1
    )

    interface.add_menu_option("Atendimento Mesas", banco.iniciar_atendimento)
    interface.add_menu_option("Autoatendimento", atm.iniciar_atendimento)

    interface.run()
    return

if __name__ == '__main__':
    main()