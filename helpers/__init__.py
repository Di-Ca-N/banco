def get_dado(mensagem, conversor=str, validador=bool, padrao=None):
    while True:
        var = input(mensagem)
        if not var and padrao:
            return padrao

        if validador(var):
            return conversor(var)
