import re


def validate_cpf(cpf):
    """
    Validates a CPF

    Args:
        cpf: string to be validated

    Returns:
        Boolean defining the received string as valid or not
    """
    regex = r'\d{11}$'  # Matches sequences of only 11 consecutive digits
    if not re.match(regex, cpf):
        print("Digite apenas os números de seu CPF")
        return False

    primeiros, verificadores = cpf[:9], cpf[9:]

    # Algorithm for validate CPF
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

    day, month, year = map(int, strdate.split("/"))

    general_invalid_day = day > 31
    general_invalid_month = month > 12
    invalid_general_february_day = day > 29 and month == 2
    invalid_february_day_not_leap = day > 28 and month == 2 and year % 4 != 0

    if general_invalid_day or general_invalid_month or invalid_general_february_day or invalid_february_day_not_leap:
        print("Data inválida")
        return False

    return True


def validate_phone(phone):
    regex = r'\(\d\d\)(\d{9}|\d{8})$'
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
