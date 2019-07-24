from contas import ContaCorrente, ContaPoupanca

conta = ContaCorrente("José", "12345")

conta.depositar(12)
conta.autenticar("12345")
conta.sacar(23)
print(conta.saldo)