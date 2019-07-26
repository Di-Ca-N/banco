from banco import Banco
from contas import ContaSuper, ContaPoupanca, ContaCorrente, Conta
from pessoa import Pessoa
from datetime import date


def main():
    jose = Pessoa("José", "27/11/2019", "1111111111", "11111111", "Rua da alegria, 27, vacaria-rs, valor", "kkkk@slal.com", "(54) 2345721")
    maria = Pessoa("Maria", "27/11/2019", "1111111111", "11111111", "Rua da alegria, 27, vacaria-rs, valor", "kkkk@slal.com", "(54) 2345721")
    sandy = Pessoa("Sandy", "27/11/2019", "1111111111", "11111111", "Rua da alegria, 27, vacaria-rs, valor", "kkkk@slal.com", "(54) 2345721")
    junior = Pessoa("Júnior", "27/11/2019", "1111111111", "11111111", "Rua da alegria, 27, vacaria-rs, valor", "kkkk@slal.com", "(54) 2345721")

    banco = Banco("Banco da Família Feliz", "0170-8")
    conta_do_jose = banco.abrir_conta(ContaPoupanca, jose,"123456")
    print(conta_do_jose)
    print(banco.abrir_conta(ContaCorrente, maria, "12343"))
    print(banco.abrir_conta(ContaSuper, sandy, "21352"))
    print(banco.abrir_conta(ContaCorrente, junior, "23134"))
    print(banco.get_contas())

    conta_gettada: Conta = banco.get_conta(conta_do_jose.identificador)
    print(conta_gettada.get_dono())
    conta_gettada.debitar(120, "ricardão")
    conta_gettada.autenticar("123456")
    conta_gettada.debitar(120, "casas bahia")
    conta_gettada.creditar(130, "José")
    conta_gettada.debitar(120, "Pedro")
    c = conta_gettada.tirar_extrato()
    print(c)
    print(conta_gettada.is_autenticado())
    print(conta_gettada.verificar_saldo())


if __name__ == '__main__':
    main()
