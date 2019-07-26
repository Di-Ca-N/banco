from datetime import datetime


class Pessoa:
    def __init__(self, nome, data_de_nascimento, cpf, rg, endereco, email, telefone):
        self.nome = nome
        self.data_de_nascimento = datetime.strptime(data_de_nascimento, "%d/%m/%Y")
        self.cpd = cpf
        self.rg = rg
        self.endereco = endereco
        self.email = email
        self.telefone = telefone

