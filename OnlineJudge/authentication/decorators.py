from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

# ==== CONSTANT KEYS  ====                                    To store the sessions with a unique name(uuid)
SESSION_NEXT_KEY = "9269b9bc-4081-40d2-ad1f-97325271fbc8"     # Key to store/acess redirect path


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
        request.session[SESSION_NEXT_KEY] = request.get_full_path()
        messages.warning(request, "Please login to continue.")
        return redirect('/login/')
    return _wrapped_view


def if_authenticated_redirect(view):
    @wraps(view)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        return view(request, *args, **kwargs)
    return _wrapped_view