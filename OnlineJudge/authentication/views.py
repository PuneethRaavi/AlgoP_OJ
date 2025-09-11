from django.shortcuts import render, redirect
from authentication.forms import UserRegistrationForm, UserLoginForm, UserForgetPasswordForm
from django.contrib.auth import login, logout, get_user_model
from django.contrib import messages
from django.conf import settings
from django.db import IntegrityError
from authentication.decorators import if_authenticated_redirect
from django.utils.crypto import get_random_string
from urllib.parse import quote, unquote
import requests


@if_authenticated_redirect
def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        try:
            if form.is_valid():
                form.save()     
                messages.success(request, "You've successfully registered. Please log in to continue.")
                return redirect('/auth/login/')
            else:
                messages.error(request, "Please fix the errors below and resubmit.")
        except IntegrityError:
                messages.error(request, "Registration failed. Please try again.")
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


@if_authenticated_redirect
def login_view(request):
    next_url = request.GET.get('next', '/')
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            login(request, form.user)
            return redirect(next_url)
    else:
        form = UserLoginForm()
    return render(request, "login.html", {"form": form, "next": next_url})


@if_authenticated_redirect
def google_login_view(request):
    client_id = settings.GOOGLE_CLIENT_ID
    redirect_uri = settings.GOOGLE_REDIRECT_URI
    next_url = request.GET.get('next', '/')

    csrf = get_random_string(16)
    request.session['google_oauth_csrf_oj_[ir7yt947g3yweir]'] = csrf
    state = f"{csrf}:{quote(next_url)}"

    auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth"
        f"?client_id={client_id}"
        f"&response_type=code"
        f"&scope=openid email profile"
        f"&redirect_uri={redirect_uri}"
        f"&state={state}"
        f"&access_type=online"
        f"&prompt=select_account"
    )
    return redirect(auth_url)


@if_authenticated_redirect
def github_login_view(request):
    client_id = settings.GITHUB_CLIENT_ID
    redirect_uri = settings.GITHUB_REDIRECT_URI
    next_url = request.GET.get('next', '/')

    csrf = get_random_string(16)
    request.session['github_oauth_csrf_oj_[ir7yt947g3yweir]'] = csrf
    state = f"{csrf}:{quote(next_url)}"

    auth_url = (
        "https://github.com/login/oauth/authorize"
        f"?client_id={client_id}"
        f"&redirect_uri={redirect_uri}"
        f"&state={state}"
        f"&scope=user:email"
        f"&allow_signup=true"
        f"&prompt=select_account"
    )
    return redirect(auth_url)


def forget_password_view(request):
    if request.method == 'POST':
        form = UserForgetPasswordForm(request.POST)
        if form.is_valid():
           form.save() 
           messages.success(request, "You've successfully changed password. Please log in to continue.")
           return redirect('/auth/login/')
    else:
        form = UserForgetPasswordForm()
    return render(request, 'forgetpassword.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, "You've been logged out successfully.")
    return redirect('/auth/login/')


@if_authenticated_redirect
def google_callback_view(request):
    state = request.GET.get("state")
    if state:
        csrf, next_url = state.split(':', 1)
        next_url = unquote(next_url)
    else:
        csrf = None
        next_url = '/'
    if not csrf or csrf != request.session.get('google_oauth_csrf_oj_[ir7yt947g3yweir]'):
        messages.error(request, "Unauthorized Request.")
        return redirect(f"/auth/login/?next={next_url}")
    
    # Handle OAuth2 error in callback
    error = request.GET.get("error")
    if error:
        if error == "access_denied":
            messages.error(request, "Google login was cancelled or denied. Please try again or use another login method.")
        else:
            messages.error(request, f"Google login failed: {error.replace('_', ' ').capitalize()}.")
        return redirect(f"/auth/login/?next={next_url}")

    code = request.GET.get("code")
    if not code:
        messages.error(request, "Google login failed: No code returned. Please try again.")
        return redirect(f"/auth/login/?next={next_url}")

    # Exchange code for token
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    r = requests.post(token_url, data=data)
    token_data = r.json()
    access_token = token_data.get("access_token")
    if not access_token:
        error_msg = token_data.get("error_description") or "Could not authenticate with Google. Please try again."
        messages.error(request, f"Google login failed: {error_msg}")
        return redirect(f"/auth/login/?next={next_url}")
    
    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v3/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}
    userinfo = requests.get(userinfo_url, headers=headers).json()

    first_name = userinfo.get("given_name", "")
    last_name = userinfo.get("family_name", "")
    email = userinfo.get("email")
    if not email:
        messages.error(request, "Google login failed: No email returned from Google.")
        return redirect(f"/auth/login/?next={next_url}")
    
    # Create or get user by Email
    User = get_user_model()
    try:
        user, created = User.objects.get_or_create(email=email, defaults={
            "username": f"{email.split('@')[0]}_{get_random_string(4)}",
            "first_name": first_name,
            "last_name": last_name,
        })
    except IntegrityError:
        messages.error(request, "Error. Please try again by filling the details manually.")
        return redirect(f"/auth/login/?next={next_url}")
    if created:
        user.set_password(get_random_string(16))
        user.save()
        # messages.success(request, "Account created via Google. Please set a password from your profile page.")

    login(request, user)
    return redirect(next_url)


@if_authenticated_redirect
def github_callback_view(request):
    state = request.GET.get("state")
    if state:
        csrf, next_url = state.split(':', 1)
        next_url = unquote(next_url)
    else:
        csrf = None
        next_url = '/'
    if not csrf or csrf != request.session.get('github_oauth_csrf_oj_[ir7yt947g3yweir]'):
        messages.error(request, "Unauthorized Request.")
        return redirect(f"/auth/login/?next={next_url}")
    
    # Handle OAuth2 error in callback
    error = request.GET.get("error")
    if error:
        if error == "access_denied":
            messages.error(request, "GitHub login was cancelled or denied. Please try again or use another login method.")
        else:
            messages.error(request, f"GitHub login failed: {error.replace('_', ' ').capitalize()}.")
        return redirect(f"/auth/login/?next={next_url}")

    code = request.GET.get("code")
    if not code:
        messages.error(request, "GitHub login failed: No code returned. Please try again.")
        return redirect(f"/auth/login/?next={next_url}")

    # Exchange code for token
    token_url = "https://github.com/login/oauth/access_token"
    data = {
        "code": code,
        "client_id": settings.GITHUB_CLIENT_ID,
        "client_secret": settings.GITHUB_CLIENT_SECRET,
        "redirect_uri": settings.GITHUB_REDIRECT_URI,
    }
    headers = {"Accept": "application/json"}
    r = requests.post(token_url, data=data, headers=headers)
    token_data = r.json()
    access_token = token_data.get("access_token")
    if not access_token:
        error_msg = token_data.get("error_description") or "Could not authenticate with GitHub. Please try again."
        messages.error(request, f"GitHub login failed: {error_msg}")
        return redirect(f"/auth/login/?next={next_url}")
    
    # Get user info
    userinfo_url = "https://api.github.com/user"
    headers = {"Authorization": f"Bearer {access_token}", "Accept": "application/vnd.github.v3+json"}
    userinfo = requests.get(userinfo_url, headers=headers).json()
    # Get user email
    email_url = "https://api.github.com/user/emails"
    emails_response = requests.get(email_url, headers=headers).json()
    email = next((e["email"] for e in emails_response if e.get("primary") and e.get("verified")), None)
    
    github_id = userinfo.get("id")
    github_username = userinfo.get("login", "")
    name = userinfo.get("name", "")
    first_name = name.split(" ")[0] if name else ""
    last_name = " ".join(name.split(" ")[1:]) if name and " " in name else ""
    
    if not github_username or not github_id:
        messages.error(request, "GitHub login failed: Required info not available.")
        return redirect(f"/auth/login/?next={next_url}")
    if not email:
        email = f"{github_id}@github.com"

    # Try to find existing user by email
    User = get_user_model()
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        username = github_username
        if User.objects.filter(username=username).exists():
            username = f"{github_username}_{get_random_string(4)}"
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=get_random_string(16)
            )
        except IntegrityError:
            messages.error(request, "Error. Please try again by filling the details manually.")
            return redirect(f"/auth/login/?next={next_url}")
    
    login(request, user)
    return redirect(next_url)


# Profile page - delete account, change password, forget password, change username, change email

