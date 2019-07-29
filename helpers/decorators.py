from functools import wraps


def auth_required(function):
    @wraps(function)
    def _function(*args, **kwargs):
        instance = args[0]
        if instance.is_autenticado():
            return function(*args, **kwargs)
        else:
            raise AttributeError("Você precisa estar autenticado para fazer essa operação")

    return _function
