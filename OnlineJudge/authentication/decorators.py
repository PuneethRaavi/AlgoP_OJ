from django.core.cache import cache
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from authentication.models import user_registrations

# ==== CONSTANT KEYS  ====                                    To store the sessions with a unique name(uuid)
SESSION_USER_ID_KEY = "2c315b19-1e35-4518-9915-9aad9170478c"  # Key to store/acess user primary key
SESSION_NEXT_KEY = "9269b9bc-4081-40d2-ad1f-97325271fbc8"     # Key to store/acess redirect path
# SESSION_PENDING_POST_KEY = "pending_post_key"                 # Key to store/access stored POST data


def public_page_context(view_func):  # Gives user context to the public page.
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        context = {}
        user_id = request.session.get(SESSION_USER_ID_KEY)
        user = None
        if user_id:
            try:
                user = user_registrations.objects.get(id=user_id)
            except user_registrations.DoesNotExist:
                pass  
        context['user'] = user
        return view_func(request, context=context, *args, **kwargs)
    return _wrapped_view



def session_check_proceed(view):           
    @wraps(view)                                              # Helps debugging(trace back to view instead of decorator)
    def _wrapped_view(request, *args, **kwargs):
        user_id = request.session.get(SESSION_USER_ID_KEY)    

        if user_id:
            try:
                request.user = user_registrations.objects.get(id=user_id)
                return view(request, *args, **kwargs)         # Continue if Authenticated
            except user_registrations.DoesNotExist:
                request.session.pop(SESSION_USER_ID_KEY, None)
                messages.warning(request, "User not found. Please register first.")
                return redirect('/register/')                 # Register if User deleted

        if request.method == "POST":                          # Incase Session expiry
            # MAX_CACHE_SIZE = 1024 * 1024  # 1MB
            # content_length = int(request.META.get("CONTENT_LENGTH") or 0)
            # if content_length <= MAX_CACHE_SIZE:              # Saves cache in DB to avoid loss of POST data
            #     key = str(uuid.uuid4())                       # Deals with small session storage limitations
            #     cache.set(f"post:{key}", {
            #         "path": request.get_full_path(),
            #         "data": dict(request.POST),
            #     }, timeout=300)  # 5 minutes
            #     request.session[SESSION_PENDING_POST_KEY] = key
            #     messages.warning(request, "Session Expired, Please login to continue your submission.")
            # else:                                             # Too large — only store the path so user can retry after login                                               
            request.session[SESSION_NEXT_KEY] = request.get_full_path()
            messages.warning(request, "Session Expired, Please login again.")
        else:                                                 
            request.session[SESSION_NEXT_KEY] = request.get_full_path()     # Saves Request path to proceed after Login
            messages.warning(request, "Please login first to continue.")    # Ensures Authenticated before accesing API

        return redirect('/login/')

    return _wrapped_view



def if_authenticated_redirect(view):
    @wraps(view)
    def _wrapped_view(request, *args, **kwargs):
        user_id = request.session.get(SESSION_USER_ID_KEY)
        if user_id:
            try:
                user_registrations.objects.get(id=user_id)
                return redirect('/')                                # Redirect to home if logged in
            except user_registrations.DoesNotExist:
                request.session.pop(SESSION_USER_ID_KEY, None)      # Remove Invalid Session
        return view(request, *args, **kwargs)                       # Continue to view if not logged in
    return _wrapped_view