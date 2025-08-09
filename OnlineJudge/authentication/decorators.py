from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from authentication.models import user_registrations  

def session_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user_id = request.session.get('ID')
        
        if not user_id:
            messages.warning(request, "Session expired or login missing. Please login again.")
            return redirect('/login/')
        
        try:
            user = user_registrations.objects.get(id=user_id)
        except user_registrations.DoesNotExist:
            messages.warning(request, "User not found. Please register again.")
            return redirect('/register/')
        
        request.custom_user = user
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view