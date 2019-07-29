class Pessoa:
    def __init__(self, nome, data_de_nascimento, cpf, rg, endereco, email, telefone):
        self.nome = nome
        self.data_de_nascimento = data_de_nascimento
        self.cpf = cpf
        self.rg = rg
        self.endereco = endereco
        self.email = email
        self.telefone = telefone

    def __str__(self):
        return self.nome
