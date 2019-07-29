import re


def validate_cpf(cpf):
    regex = r'\d{11}$'
    if not re.match(regex, cpf):
        print("Digite apenas os números de seu CPF")
        return False

    primeiros, verificadores = cpf[:9], cpf[9:]

    for i in [0, 1]:
        multiplicador = 10 + i
        total = 0
        for j in range(9 + i):
            total += int(primeiros[j]) * multiplicador
            multiplicador -= 1
        digito = total * 10 % 11

        if digito != int(verificadores[i]):
            print("CPF inválido")
            return False

        primeiros += verificadores[0]

    return True


def validate_email(email):
    regex = r'[\w\.]+@[\w\.]+\.\w'

    if not re.match(regex, email):
        print("Email inválido")
        return False
    return True


def validate_date(strdate):
    regex = r'\d\d/\d\d/\d\d\d\d$'
    if not re.match(regex, strdate):
        print("A data deve estar no formato dd/mm/aaaa")
        return False
    return True


def validate_phone(phone):
    regex = r'\(\d\d\)((\d{5}|\d{4})\-\d{4})$'
    if not re.match(regex, phone):
        print("Telefone deve ter o formato (XX)XXXXXXXX ou (XX)XXXXXXXXX")
        return False
    return True

def validate_cep(cep):
    regex = r'\d{5}-\d{3}$'
    if not re.match(regex, cep):
        print("O CEP é inválido. Ele deve estar no formato XXXXX-XXX")
        return False
    return True
