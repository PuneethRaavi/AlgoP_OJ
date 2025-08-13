from django.shortcuts import render, redirect
from authentication.forms import UserRegistrationForm, UserLoginForm, UserForgetPasswordForm
from django.contrib import messages
from django.db import IntegrityError
from django.core.cache import cache
from authentication.decorators import SESSION_USER_ID_KEY, SESSION_NEXT_KEY, if_authenticated_redirect


@if_authenticated_redirect
def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        try:
            if form.is_valid():
                form.save()     # Database violation is any will rise in page 
                messages.success(request, "You've successfully registered. Please log in to continue.")
                return redirect('/login/')
            else:
                messages.error(request, "Please fix the errors below and resubmit.")
                # Inbuilt - form with field and nonfield validation errors will be displayed in the template
        except IntegrityError:  # Handles simaltaneous same username registration
                 messages.error(request, "A user with that username already exists. Please choose a different one.")
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})


@if_authenticated_redirect
def login_view(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = form.user    # Retrieved in form's clean()

            request.session[SESSION_USER_ID_KEY] = user.id    # Save session
            if request.session.get(SESSION_USER_ID_KEY) != user.id:   # Verify session save
                messages.error(request,"Session error: Could not log you in. Please try again in a few minutes.")
                return redirect("/login/?retry=1")

            # login_request_post = request.session.pop(SESSION_PENDING_POST_KEY, None)
            # if login_request_post:
            #     post_data = cache.get(f"post:{login_request_post}")
            #     if post_data:
            #         cache.delete(f"post:{login_request_post}")
            #         # Here you could actually re-trigger the view logic with POST data
            #         return redirect(post_data["path"])          # ERROR - This does not send post data

            login_request_get = request.session.pop(SESSION_NEXT_KEY, "/")    # Redirect to next path or by default home
            return redirect(login_request_get)
    else:
        form = UserLoginForm()
        
        if request.GET.get("retry"):   # Helpful when previous session error
            messages.warning(request,"We couldn't log you in previously due to a temporary issue. Please try again.")

    return render(request, "login.html", {"form": form})



def forget_password_view(request):
    if request.method == 'POST':
        form = UserForgetPasswordForm(request.POST)
        if form.is_valid():
           form.save() 
           messages.success(request, "You've successfully changed password. Please log in to continue.")
           return redirect('/login/')
    else:
        form = UserForgetPasswordForm()

    return render(request, 'forgetpassword.html', {'form': form})



def logout_view(request):
    request.session.flush()     # Clears the session data
    messages.success(request, "You've been logged out successfully.")
    return redirect('/login/')