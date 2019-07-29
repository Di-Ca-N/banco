import random
import time
from datetime import date

from contas import Conta, ContaAdministrativa, ContaCorrente, ContaPoupanca
from cadastros.endereco import Endereco
from cadastros.pessoa import Pessoa
from helpers import validators, converters, get_dado


def gerar_senha():
    a = 1
    while True:
        yield "{:03}".format(a)
        a += 1


def gerar_identificador():
    return "{}{}.{}{}{}-{}".format(*random.sample(range(1, 10), 6))


class Banco:
    nome = ""
    identificador = ""
    contas = {}

    def __init__(self, nome, identificador):
        self.nome = nome
        self.identificador = identificador
        self.contas = {}

    def iniciar_atendimento(self):
        print("Sua senha é {}".format(next(gerar_senha())))
        print("Aguarde para ser atendido...")
        time.sleep(3)
        while True:
            opcao = input("""
        XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
        XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
        XX                BANCO DA FAMÍLIA FELIZ                XX
        XX    Onde você, cliente, é nosso maior patrimônio!     XX
        XX                                                      XX
        XX  01. Abrir Conta                                     XX
        XX  02. Encerrar Conta                                  XX
        XX  03. Logar como Administrador                        XX
        XX  X. Sair                                             XX
        XX                                                      XX
        XX                                                      XX
        XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
        """)

            while opcao not in ["01", "02", "03","X"]:
                opcao = input("Digite uma opção válida")

            if opcao == "01":
                self.atendimento_abrir_conta()
            elif opcao == "02":
                self.atendimento_encerrar_conta()
            elif opcao == "03":
                self.atendimento_logar_admin()
            else:
                return

    def atendimento_abrir_conta(self):
        dono = self.get_dados_cliente()
        senha = input("Informe uma senha")
        tipo = self.get_tipo_de_conta()
        if tipo:
            conta = self.abrir_conta(tipo, dono, senha)
            print("Conta criada! Seu número é {}".format(conta.identificador))

    def get_tipo_de_conta(self):
        tipo = input("""
        XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
        XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
        XX                BANCO DA FAMÍLIA FELIZ                XX
        XX                    Tipo de Conta                     XX
        XX                                                      XX
        XX  01. Conta Corrente                                  XX
        XX  02. Conta Poupanca                                  XX
        XX  03. Conta Administrativa                            XX
        XX  X. Sair                                             XX
        XX                                                      XX
        XX                                                      XX
        XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
        """)
        while tipo not in ["01", "02", "03", "X"]:
            tipo = input("Opção inválida!")

        if tipo == "01":
            return ContaCorrente
        elif tipo == "02":
            return ContaPoupanca
        elif tipo == "03":
            return ContaAdministrativa
        else:
            return

    def get_dados_cliente(self):
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

    def abrir_conta(self, tipo_conta, dono, senha, identificador=gerar_identificador()):
        while identificador in self.contas:
            identificador = gerar_identificador()

        if issubclass(tipo_conta, Conta):
            conta = tipo_conta(identificador, dono, senha)
            self.contas[identificador] = conta

            return conta

        else:
            raise TypeError("'tipo_conta' deve ser uma subclasse de 'Conta'")

    def atendimento_encerrar_conta(self):
        identificador = input("Identificador: ")
        senha = input("Senha: ")
        self.encerrar_conta(identificador, senha)

    def encerrar_conta(self, identificador, senha):
        conta = self.get_conta(identificador)

        if conta is not None and conta.autenticar(senha):
            if conta.fechar():
                del self.contas[identificador]
            else:
                print("Não foi possível encerrar a conta!")
        else:
            print("Credenciais incorretas")

    def get_contas(self):
        return self.contas.keys()

    def get_conta(self, identificador):
        return self.contas.get(identificador, None)

    def corrigir_contas(self, data_atual: date):
        dia_atual = data_atual.day
        mes_autal = data_atual.month
        ano_atual = data_atual.year

        for conta in self.contas.values():
            data_criacao = conta.criacao
            if dia_atual == data_criacao.day and (mes_autal != data_criacao.month or ano_atual != data_criacao.year):
                conta.corrigir()

    def atendimento_logar_admin(self):
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
