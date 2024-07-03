from functools import wraps
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

def supplier_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_supplier:
            return redirect(settings.LOGIN_URL)
        return view_func(request, *args, **kwargs)
    return wrapper
