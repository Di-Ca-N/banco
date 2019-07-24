from functools import wraps

def auth_required(function):
	@wraps(function)
	def _function(*args, **kwargs):
		if args[0].autenticado:
			function(*args, **kwargs)
		else:
			print("não autenticado")
			#raise AttributeError("Você precisa estar autenticado!")

	return _function
