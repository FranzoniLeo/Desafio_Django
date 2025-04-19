from django.shortcuts import redirect
from functools import wraps

def decorador_g(cargo):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')  #retorna o usuario não logado a pagina de login

            if not hasattr(request.user, 'perfil'):
                return redirect('login')  #confirmar que o usuario tem um perfil 

            if request.user.perfil.tipo != cargo:
                return redirect('login')  #retorna o usuario a pagina de login se o mesmo não tiver o cargo necessario

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


#Decoradores específicos por tipo

def apenas_admin(view_func):
    return decorador_g('admin')(view_func)

def apenas_staff(view_func):
    return decorador_g('staff')(view_func)