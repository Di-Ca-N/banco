def get_dado(mensagem, conversor=str, validador=bool, padrao=None):
    """
    Solicita um dado para o usuário e repete até receber um dado válido

    Args:
        mensagem: Mesagem para solicitar o dado
        conversor: Função que converte o valor recebido
        validador: Função que verifica se o valor recebido é valido, retornando um booleano
        padrao: Valor padrão para o dado

    Returns:
        Dado solicitado, já convertido
    """
    while True:
        var = input(mensagem)
        if not var and padrao is not None:
            return padrao

        try:
            if validador(var):
                return conversor(var)
        except:
            print("Dado Inválido")
