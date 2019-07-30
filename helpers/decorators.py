from functools import wraps


def auth_required(function):
    """
    Decorador para requerir autenticação prévia da conta para executar determinadas ações

    Args:
        function: função a ser decorada. Sempre um método de Conta ou uma de suas subclasses

    Returns:
        Executa a função decorada, caso a conta esteja autenticada

    Raises:
        AttributeError: caso a conta não esteja autenticada
    """
    @wraps(function)
    def _function(*args, **kwargs):
        instance = args[0]
        if instance.autenticado:
            return function(*args, **kwargs)
        else:
            raise AttributeError("Você precisa estar autenticado para fazer essa operação")

    return _function
