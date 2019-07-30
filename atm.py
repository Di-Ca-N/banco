from datetime import datetime
from helpers.interface import Interface


class ATM:
    """
    Cria uma ATM e gerencia o atendimento dos clientes

    Attributes:
        dinheiro: Dicionário contendo as notas e a quantidade de cada nota
        historico: Lista contendo as operações realizadas na ATM
        conta_autenticada: objeto Conta que está atualmente autenticado na máquina
    """
    def __init__(self, banco):
        """
        Inicializa uma ATM

        Args:
            banco: Objeto Banco que a ATM utilizirá para acessar as contas cadastradas
        """
        self.dinheiro = {2: 0, 5: 0, 10: 0, 20: 0, 50: 0, 100: 0}
        self.historico = []
        self.conta_autenticada = None
        self.banco = banco

    def iniciar_atendimento(self):
        """
        Realiza o atendimento de um usuário

        Returns:
            None
        """
        interface = Interface(
            title="BANCO DA FAMÍLIA FELIZ",
            message="Onde você, cliente, é o nosso maior patrimômio!",
            box_weight=2,
            bottom_weight=1,
            bottom_padding=1
        )

        interface.add_menu_option("Entrar na conta", self.atender_entrada)
        interface.add_menu_option("Realizar depósito", self.atender_deposito)

        interface.run()

    def atender_entrada(self):
        """
        Atende a requisições para entrar em uma conta

        Returns:
            None
        """
        identificador = input("Identificador da conta: ")
        senha = input("Senha: ")
        self.conectar_conta(identificador, senha)

    def atender_deposito(self):
        """
        Atende a requisições para fazer depósito

        Returns:
            None
        """
        tipo = "DEPÓSITO"
        conta_destino = self.conta_autenticada if self.conta_autenticada else \
            self.banco.get_conta(input("Conta destino: "))
        depositante = self.conta_autenticada if self.conta_autenticada else input("Depositante: ")
        valor = float(input("Valor: "))
        if self.deposito(conta_destino, depositante, valor):
            self.gravar_historico(tipo, valor, depositante, conta_destino, datetime.now())
        else:
            print("Não foi possível realizar o depósito")

    def conectar_conta(self, identificador, senha):
        """
        Busca uma conta pelo identificador no banco e tenta autenticar utilizando a senha informada

        Args:
            identificador: Identificador da conta
            senha: Senha de acesso para logar

        Returns:
            None
        """
        conta = self.banco.get_conta(identificador)

        if conta is not None:
            if conta.autenticar(senha):
                self.conta_autenticada = conta

                if self.conta_autenticada.superuser:
                    self.atender_gerente()
                else:
                    self.atender_cliente()
        else:
            print("Não foi possível entrar. Por favor, confira os dados informados.")

    def atender_gerente(self):
        """
        Atende a logins de contas administrativas

        Returns:
            None
        """
        interface = Interface(
            title="BANCO DA FAMÍLIA FELIZ",
            message="Trabalhe, escravo, trabalhe!",
            box_weight=2,
            bottom_weight=1,
            bottom_padding=1
        )

        interface.add_menu_option("Saldar ATM", self.listar_notas)
        interface.add_menu_option("Resetar ATM", self.reset)
        interface.add_menu_option("Listar operações recentes", self.mostrar_historico)
        interface.add_menu_option("Depositar na ATM", self.adicionar_dinheiro)

        interface.run()
        self.desconectar_conta()

    def atender_cliente(self):
        """
        Atende a logins de contas comuns

        Returns:
            None
        """
        interface = Interface(
            title="BANCO DA FAMÍLIA FELIZ",
            message="Sua felicidade é nossa maior prioridade!",
            box_weight=2,
            bottom_weight=1,
            bottom_padding=1
        )

        interface.add_menu_option("Saque", self.atender_saque)
        interface.add_menu_option("Depósito", self.atender_deposito)
        interface.add_menu_option("Transferência", self.atender_transferencia)
        interface.add_menu_option("Extrato", self.fornecer_extrato)
        interface.add_menu_option("Saldo", self.fornecer_saldo)

        interface.run()
        self.desconectar_conta()

    def desconectar_conta(self):
        """
        Desconecta a conta logada atualmente

        Returns:
            None
        """
        self.conta_autenticada.deslogar()
        self.conta_autenticada = None
        print("Você não está mais conectado.")

    def listar_notas(self):
        """
        Lista as notas atualmente na ATM

        Returns:
            None
        """
        relatorio_notas = ""
        if self.dinheiro:
            for nota, quantidade in self.dinheiro.items():
                relatorio_notas += "Valor: R${:6.2f} | Quantidade: {} \n".format(nota, quantidade)
        else:
            relatorio_notas = "Não há notas no caixa"

        print(relatorio_notas)

    def reset(self):
        """
        Reseta a ATM

        Returns:
            None
        """
        lavagemdedinheiro = input("Você tem absoluta certeza do que está fazendo? S/N")
        if lavagemdedinheiro == "S" or lavagemdedinheiro == "s":
            self.dinheiro = {}
            self.historico = []

    def mostrar_historico(self):
        """
        Mostra o histórico de operações da ATM

        Returns:
            None
        """
        for evento in self.historico:
            print(evento)

    def adicionar_dinheiro(self):
        """
        Adiciona dinheiro

        Returns:
            None
        """
        pergunta = "S"
        tipo, destino = "DEPOSITO", "ATM"

        while pergunta == "S":
            nota = int(input("Qual o valor da nota selecionada? \n"))
            qntd = int(input("Quantas notas? \n"))
            self.adicionar_notas(nota, qntd)
            self.gravar_historico(tipo, nota * qntd, "BANCO", destino, datetime.now())
            pergunta = input("Você ainda quer depositar mais dinheiro? S/N \n").upper()

    def adicionar_notas(self, nota, qtd):
        """
        Adiciona notas em determinadas quantidades

        Args:
            nota: valor da nota que será adicionada. Deve ser um valor válido, já cadastrado no atributo dinheiro
            qtd: quantidade da nota que será adicionada

        Returns:
            None
        """
        if nota in self.dinheiro:
            self.dinheiro[nota] += qtd
        else:
            print("Valor de nota não existe")

    def gravar_historico(self, tipo, valor, conta_origem, conta_destino, data):
        """
        Grava as operações realizadas na ATM em seu histórico

        Args:
            tipo: Tipo de operação realizada
            valor: Valor envolvido na operação
            conta_origem: Origem da operação
            conta_destino: Destino da operação
            data: Data da operação

        Returns:
            None
        """
        evento = "OPERAÇÃO: {} | VALOR: R$ {} | CONTA DE ORIGEM: {} | CONTA DESTINO: {} | DATA: {}"\
            .format(tipo, valor, conta_origem, conta_destino, data)
        self.historico.append(evento)

    def atender_saque(self):
        """
        Atende à requisições para fazer saques

        Returns:
            None
        """
        tipo = "SAQUE"
        valor = float(input("Valor solicitado:"))
        if self.saque(self.conta_autenticada, valor):
            self.gravar_historico(tipo, valor, self.conta_autenticada, None, datetime.now())
        else:
            print("Ocorreu um problema durante a transação. Cheque as informações solicitadas e o saldo da conta.")

    def saque(self, conta_origem, valor):
        """
        Realiza um saque, verificando se é possível realizar o pagamento com as notas disponíveis

        Args:
            conta_origem: Conta de onde será realizado o saque
            valor: Valor a ser depositado

        Returns:
            Booleano indicando se o saque ocorreu com sucesso
        """
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

    def deposito(self, conta_destino, depositante, valor):
        """
        Realiza um depósito

        Args:
            conta_destino: Conta para onde irá o valor depositado
            depositante: Quem realizou o depósito
            valor: Valor depositado

        Returns:
            Booleano indicando se o depósito ocorreu com sucesso
        """
        try:
            conta_destino.creditar(valor, str(depositante))
            return True

        except ValueError as erro:
            print(erro.args[0])
            return False

    def atender_transferencia(self):
        """
        Atende a requisições para fazer transferências

        Returns:
            None
        """
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

    def fornecer_extrato(self):
        """
        Atende a requisições para fornecer extratos

        Returns:
            None
        """
        extrato_conta = self.conta_autenticada.get_extrato()
        print(extrato_conta)

    def fornecer_saldo(self):
        """
        Atende a requisições para informar saldo

        Returns:
            None
        """
        saldo_conta = self.conta_autenticada.get_saldo()
        print("Seu saldo é R${:.2f}".format(saldo_conta))
