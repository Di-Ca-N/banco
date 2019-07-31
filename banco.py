import random
import time
from datetime import date
from dateutil.relativedelta import relativedelta

from contas import Conta, ContaAdministrativa, ContaCorrente, ContaPoupanca
from cadastros.endereco import Endereco
from cadastros.pessoa import Pessoa
from helpers import validators, converters, get_dado
from helpers.interface import Interface


def gerador_senha():
    """
    Gera senhas em sequência, partindo de "001"

    Returns:
        Senha de três dígitos como string
    """
    a = 1
    while True:
        yield "{:03}".format(a)
        a += 1
        

def gerar_identificador():
    """
    Gera um identficador aleatória para uma conta

    Returns:
        Código da conta no formato "XX.XXX-X"
    """
    return "{}{}.{}{}{}-{}".format(*random.sample(range(1, 10), 6))


class Banco:
    """
    Gerenciamento de funções relativas a um banco

    Attributes:
        nome: Nome do banco
        identificador: Identificado único do banco
        contas: Dicionário contendo as contas cadastradas no banco, contendo seus identificadores como chaves
        gerador_de_senhas: Objeto responsável por gerar as senhas do banco
    """

    def __init__(self, nome, identificador):
        """
        Inicializa um banco

        Args:
            nome: Nome do banco
            identificador: Identificador do banco
        """
        self.nome = nome
        self.identificador = identificador
        self.contas = {}
        self.gerador_de_senhas = gerador_senha()

    def iniciar_atendimento(self):
        """
        Inicia o atendimento

        Returns:
            None
        """
        print("Sua senha é {}".format(next(self.gerador_de_senhas)))
        print("Aguarde para ser atendido...")
        time.sleep(3)

        interface = Interface(
            title="BANCO DA FAMÍLIA FELIZ",
            message="Aquilo que é seu, é nosso!",
            box_weight=2,
            bottom_weight=1,
            bottom_padding=1
        )

        interface.add_menu_option("Abrir conta", self.atendimento_abrir_conta)
        interface.add_menu_option("Encerrar conta", self.atendimento_encerrar_conta)
        interface.add_menu_option("Logar como administrador", self.atendimento_logar_admin)

        interface.run()
        return

    def atendimento_abrir_conta(self):
        """
        Realiza o atendimento para abrir uma conta

        Returns:
            None
        """
        dono = self.get_dados_cliente()
        tipo = self.get_tipo_de_conta()
        senha = input("Informe uma senha: ")
        if tipo:
            conta = self.abrir_conta(tipo, dono, senha)
            print("Conta criada! Seu número é {}".format(conta.identificador))

    @staticmethod
    def get_dados_cliente():
        """
        Solicita os dados para a criação de um objeto Pessoa e o cria

        Returns:
            Objeto Pessoa com os dados informados
        """
        print("Informe seus dados pessoais")
        nome = get_dado("Nome: ")
        data_de_nascimento = get_dado("Data de Nascimento (dd/mm/aaaa): ", converters.str_to_date,
                                      validador=validators.validate_date)
        cpf = get_dado("CPF: ", validador=validators.validate_cpf)
        rg = get_dado("RG: ")
        email = get_dado("E-Mail: ", validador=validators.validate_email)
        telefone = get_dado("Telefone: ", validador=validators.validate_phone)

        print("Informe seus dados de endereço: ")
        pais = get_dado("País: ")
        estado = get_dado("Estado: ")
        cidade = get_dado("Cidade: ")
        bairro = get_dado("Bairro: ")
        rua = get_dado("Rua: ")
        numero = get_dado("Número: ")
        complemento = get_dado("Complemento (opcional): ", padrao="")
        cep = get_dado("CEP: ")

        endereco = Endereco(pais, estado, cidade, bairro, rua, numero, complemento, cep)

        return Pessoa(nome, data_de_nascimento, cpf, rg, endereco, email, telefone)

    @staticmethod
    def get_tipo_de_conta():
        """
        Apresenta opções para selecionar um tipo de conta para ser aberta

        Returns:
            Subclasse de Conta
        """
        interface = Interface(
            title="BANCO DA FAMÍLIA FELIZ",
            message="Escolha o tipo de conta",
            box_weight=2,
            bottom_weight=1,
            bottom_padding=1,
            return_selected_option=True,
        )
        interface.add_menu_option("Conta Corrente", ContaCorrente)
        interface.add_menu_option("Conta Poupanca", ContaPoupanca)
        interface.add_menu_option("Conta Administrativa", ContaAdministrativa)

        tipo_selecionado = interface.run()

        return tipo_selecionado

    def abrir_conta(self, tipo_conta, dono, senha, identificador=gerar_identificador(), **kwargs):
        """
        Abre uma conta com o tipo informado

        Args:
            tipo_conta: Tipo de conta que deve ser aberta. Deve ser uma subclasse de Conta
            dono: Dono da conta. Deve ser um objeto Pessoa
            senha: Senha de acesso à conta
            identificador: Identificador único para a conta. Se não for definido, é gerado um identificador aleatório
            **kwargs: argumentos extras para a criação da conta, dependentes do tipo de conta

        Returns:
            Conta

        Raises:
            TypeError se o tipo de conta informado não for uma subclasse de Conta
        """
        while identificador in self.contas:
            identificador = gerar_identificador()

        if issubclass(tipo_conta, Conta):
            conta = tipo_conta(identificador, dono, senha, **kwargs)
            self.contas[identificador] = conta

            return conta

        else:
            raise TypeError("'tipo_conta' deve ser uma subclasse de 'Conta'")

    def atendimento_encerrar_conta(self):
        """
        Realiza o atendimento para encerrar uma conta

        Returns:
            None
        """
        identificador = input("Identificador: ")
        senha = input("Senha: ")
        self.encerrar_conta(identificador, senha)

    def encerrar_conta(self, identificador, senha):
        """
        Encerra a conta indicada, se a senha estiver correta

        Args:
            identificador: Identificador da conta
            senha: Senha de acesso à conta

        Returns:
            None
        """
        conta = self.get_conta(identificador)

        if conta is not None and conta.autenticar(senha):
            if conta.fechar():
                del self.contas[identificador]
            else:
                print("Não foi possível encerrar a conta!")
        else:
            print("Credenciais incorretas")

    def get_conta(self, identificador):
        """
        Procura uma conta pelo identificador. Se existir, a retorna. Caso contrário, retorna None

        Args:
            identificador: Identificador da conta

        Returns:
            Conta, caso exista. None, caso contrário
        """
        return self.contas.get(identificador, None)

    def corrigir_contas(self, data_atual):
        """
        Corrige os valores presentes em todas as contas do banco

        Args:
            data_atual: Data corrente, utilizada para calcular as correções das contas.

        Returns:
            None
        """
        um_mes = relativedelta(months=1)
        for conta in self.contas.values():
            if not conta.superuser:
                ultima_correcao = conta.ultima_correcao
                while ultima_correcao + um_mes < data_atual:
                    conta.corrigir()
                    ultima_correcao += um_mes
                conta.ultima_correcao = ultima_correcao
                print("A conta {} foi corrigida! Agora possui saldo de R${:.2f}".format(conta.identificador, conta.saldo))

    def atendimento_logar_admin(self):
        """
        Realiza o atendimento para logar uma conta administrativa

        Returns:
            None
        """
        identificador = input("Indentificador: ")
        senha = input("Senha: ")

        conta = self.get_conta(identificador)

        if conta is not None and conta.autenticar(senha):
            if conta.is_superuser():
                opcao = input("Deseja corrigir os valores das contas? (S/N)").upper()

                if opcao == "S":
                    data = get_dado("Data (dd/mm/aaaa)(Deixe em branco para usar a data atual): ",
                                    converters.str_to_date, validators.validate_date, date.today())
                    self.corrigir_contas(data)

            else:
                print("Conta não é administrativa!")
        else:
            print("Senha incorreta!")
