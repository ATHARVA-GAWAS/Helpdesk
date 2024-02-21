from functools import wraps
from django.shortcuts import redirect


def custom_login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login/')  # Replace 'custom_login' with your custom login URL name
        return view_func(request, *args, **kwargs)
    return _wrapped_view