from functools import wraps
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied


def in_group(user, name: str) -> bool:
    return user.is_authenticated and user.groups.filter(name=name).exists()


def require_group(name: str):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if in_group(request.user, name):
                return view_func(request, *args, **kwargs)
            if request.user.is_authenticated:
                raise PermissionDenied
            return redirect_to_login(request.get_full_path(), "/accounts/login/")

        return _wrapped

    return decorator
