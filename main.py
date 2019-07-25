from operacao import Operacao
from itertools import groupby

ops = [
	Operacao("+", 40, "123458-7", "27/03/2018"),
	Operacao("-", 40, "123356-6", "27/03/2018"),
	Operacao("-", 80, "123256-6", "27/03/2018"),
	Operacao("+", 20, "121456-5", "27/03/2018"),
	Operacao("+", 120, "123456-8", "28/03/2018"),
	Operacao("-", 140, "123456-6", "28/03/2018"),
	Operacao("+", 160, "123456-6", "29/03/2018"),
]

g = groupby(sorted(ops, key=lambda x: (x.data, x.tipo)), lambda x: x.data)

for data, grupo in g:
	print("Operações em {}".format(data))
	for operacao in grupo:
		print(operacao)