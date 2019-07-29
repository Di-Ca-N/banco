from datetime import datetime
from interface import Interface

class Atm:
    dinheiro = {}
    historico = []
    conta_autenticada = None
    banco = None

    def __init__(self, banco):
        self.dinheiro = {2: 1000, 5: 1000, 10: 1000, 20: 1000, 50: 1000, 100: 1000}
        self.historico = []
        self.conta_autenticada = None
        self.banco = banco

    # def iniciar_atendimento(self):
    #     while True:
    #         if self.conta_autenticada is None:
    #             self.iniciar_atendimento()
    #         elif self.conta_autenticada.is_superuser():
    #             self.atender_gerente()
    #         else:
    #             self.atender_cliente()

    def iniciar_atendimento(self):
        while True:
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
                return

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
                nota = int(input("Qual o valor da nota selecionada? \n"))
                qntd = int(input("Quantas notas? \n"))
                self.adicionar_dinheiro(nota, qntd)
                self.gravar_historico(tipo, nota * qntd, "BANCO", destino, datetime.now())
                pergunta = input("Você ainda quer depositar mais dinheiro? S/N \n").upper()

        elif alternativa == "X":
            self.desconectar_conta()

    def atender_cliente(self):
        while True:
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
                conta_destino = self.banco.get_conta(input("Conta destino: "))
                if conta_destino is not None:
                    try:
                        valor = float(input("Valor a transferir: R$ "))
                        self.conta_autenticada.debitar(valor, str(conta_destino))
                        conta_destino.creditar(valor, str(self.conta_autenticada))
                        self.gravar_historico(tipo, valor, self.conta_autenticada, conta_destino, datetime.now())

                    except ValueError as e:
                        print(e.args[0])
                        print("A transferência do valor solicitado não pôde ser concluída. Verifique suas informações, parça.")

                else:
                    print("A conta solicitada não existe")

            elif alternativa == "04":
                print(self.fornecer_extrato(self.conta_autenticada))

            elif alternativa == "05":
                print("Seu saldo é R${:.2f}".format(self.fornecer_saldo(self.conta_autenticada)))

            elif alternativa == "X":
                self.desconectar_conta()
                return

    def listar_notas(self):
        relatorio_notas = ""
        if self.dinheiro:
            for nota, quantidade in self.dinheiro.items():
                relatorio_notas += "Valor: R${:6.2f} | Quantidade: {} \n".format(nota, quantidade)
        else:
            relatorio_notas = "Não há notas no caixa"

        print(relatorio_notas)

    def mostrar_historico(self):
        for evento in self.historico:
            print(evento)

    def gravar_historico(self, tipo, valor, conta_origem, conta_destino, data):
        evento = "OPERAÇÃO: {} | VALOR: R$ {} | CONTA DE ORIGEM: {} | CONTA DESTINO: {} | DATA: {}".format(tipo, valor, conta_origem, conta_destino, data)
        self.historico.append(evento)

    def adicionar_dinheiro(self, nota, qtd):
        if nota in self.dinheiro:
            self.dinheiro[nota] += qtd
        else:
            print("Valor de nota não existe")

    def reset(self):
        self.dinheiro = {}
        self.historico = []

    def conectar_conta(self, identificador, senha):
        conta = self.banco.get_conta(identificador)
        if conta is not None:
            if conta.autenticar(senha):
                self.conta_autenticada = conta

                if self.conta_autenticada.is_superuser():
                    self.atender_gerente()
                else:
                    self.atender_cliente()
        else:
            print("Não foi possível entrar. Por favor, confira os dados informados.")

    def desconectar_conta(self):
        self.conta_autenticada.deslogar()
        self.conta_autenticada = None
        print("Você não está mais conectado.")

    def saque(self, conta_origem, valor):
        try:
            falta = valor
            necessarias = {100: 0, 50: 0, 20: 0, 10: 0, 5: 0, 2: 0}
            for nota in [100, 50, 20, 10, 5, 2]:
                for contador in range(self.dinheiro[nota]):
                    if falta >= nota:
                        falta -= nota
                        necessarias[nota] += 1

            if falta == 0:
                conta_origem.debitar(valor, str(conta_origem))
                for nota in necessarias:
                    self.dinheiro[nota] -= necessarias[nota]
                return True

            else:
                print("Não é possível pagar a quantia especificada")
                return False

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
