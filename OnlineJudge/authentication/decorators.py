from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def public_page_context(view_func):
    @wraps(view_func)                                         # Helps debugging(trace back to view instead of decorator)
    def _wrapped_view(request, *args, **kwargs):
        context = {}
        user = request.user if request.user.is_authenticated else None
        context['user'] = user
        return view_func(request, context=context, *args, **kwargs)
    return _wrapped_view


def session_check_proceed(view):           
    @wraps(view)                                              
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view(request, *args, **kwargs)
        next_url=request.get_full_path()
        messages.warning(request, "Please login to continue.")
        return redirect(f'/auth/login/?next={next_url}')
    return _wrapped_view


def if_authenticated_redirect(view):
    @wraps(view)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        return view(request, *args, **kwargs)
    return _wrapped_view