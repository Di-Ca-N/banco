from dataclasses import dataclass
from datetime import date

@dataclass
class Pessoa:
	nome: str
	data_de_nascimento: date
	cpf: str
	rg: str
	endereco: str
	email: str
	telefone: str
