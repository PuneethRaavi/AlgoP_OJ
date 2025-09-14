from django.shortcuts import render, redirect
from authentication.models import OTP
from authentication.forms import UserRegistrationForm, UserLoginForm, UserForgetPasswordForm, UserResetPasswordForm
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.conf import settings
from django.db import IntegrityError
from django.http import JsonResponse
from authentication.decorators import if_authenticated_redirect
from django.utils.crypto import get_random_string
from urllib.parse import quote, unquote
from .utils import send_otp_email
import requests
from datetime import timedelta
from django.utils import timezone


@if_authenticated_redirect
def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        try:        # try/except used to catch any unexpected errors (send otp fails, db error, etc)
            if form.is_valid():
                check_otp_limit = OTP.objects.filter(email=form.cleaned_data['email'], purpose='registration', is_verified=False, expires_at__gt=timezone.now()).order_by('-created_at')
                if check_otp_limit.count() >= 3:
                    messages.error(request, "Too many OTP requests. Please try again after some time.")
                    return redirect('register')
                otp_instance = OTP.objects.create(
                    email=form.cleaned_data['email'],
                    purpose='registration',
                    otp=get_random_string(6, allowed_chars='0123456789')
                )
                request.session['registration_data_ydghfi78a6ftg8afy'] = form.cleaned_data
                send_otp_email(otp_instance.email, otp_instance.otp, 'registration')
                return redirect('verify_registration')
        except IntegrityError:
            messages.error(request, "Registration failed. Please try again after some time.")
    else:
        if 'registration_data_ydghfi78a6ftg8afy' in request.session:
            form = UserRegistrationForm(request.session['registration_data_ydghfi78a6ftg8afy'])
            del request.session['registration_data_ydghfi78a6ftg8afy']
        else:
            form = UserRegistrationForm()
            
    return render(request, 'register.html', {'form': form})


@if_authenticated_redirect 
def verify_registration(request):
    registration_data = request.session.get('registration_data_ydghfi78a6ftg8afy')
    if not registration_data:
        messages.error(request, "Registration session expired. Please register again.")
        return redirect('register')
    try:
        if request.method == 'POST':
            action = request.POST.get('action', 'verify')
            if action == 'resend':
                check_otp_limit = OTP.objects.filter(email=registration_data['email'], purpose='registration', is_verified=False, expires_at__gt=timezone.now()).order_by('-created_at')
                if check_otp_limit.count() >= 3:
                    request.session.pop('registration_data_ydghfi78a6ftg8afy', None)
                    messages.error(request, "Too many OTP requests. Please try again after some time.")
                    return JsonResponse({'success': False, 'redirect': '/auth/register/'})
                otp_instance = OTP.objects.create(email=registration_data['email'], purpose='registration', otp=get_random_string(6, allowed_chars='0123456789'))
                send_otp_email(otp_instance.email, otp_instance.otp, 'registration')
                return JsonResponse({'success': True, 'message': 'A new OTP has been sent to your email.'}) 
            otp_entered = request.POST.get('otp')
            otp_obj = OTP.get_latest_valid(registration_data['email'], 'registration')
            if not otp_obj:
                messages.error(request, "No valid OTP found. Please request a new one.")
            elif otp_obj.otp != otp_entered:
                messages.error(request, "Invalid OTP. Please try again.")
            else:  # OTP is valid, Create user
                form = UserRegistrationForm(registration_data)
                if form.is_valid():
                    user = form.save()
                    otp_obj.mark_verified()
                    del request.session['registration_data_ydghfi78a6ftg8afy']
                    login(request, user)
                    return redirect('/') 
                else:
                    messages.error(request, "An error occurred during registration. Please try again.")
                    return redirect('register')
    except Exception:
        messages.error(request, "An error occurred. Please try again after some time.")
        return redirect('register')

    context = {
        'email': registration_data['email'],
        'username': registration_data['username'],
    }
    return render(request, 'register_verification.html', context)


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

@if_authenticated_redirect
def forget_password_view(request):
    if request.method == 'POST':
        form = UserForgetPasswordForm(request.POST)
        try:
            if form.is_valid():
               check_active_otp = OTP.get_latest_valid(form.cleaned_data['email'], 'password_reset')
               if check_active_otp:
                     messages.warning(request, "A link has already been sent to your email. Please check your inbox/ spam folder or try again after some time.")
                     return redirect('forget_password')
               otp_instance = OTP.objects.create(email=form.cleaned_data['email'], purpose='password_reset', otp=get_random_string(6, allowed_chars='0123456789'), temp_data={"token": get_random_string(32)}, expires_at = timezone.now() + timedelta(minutes=60))
               link = f"{request.scheme}://{request.get_host()}/auth/reset-password/?email={otp_instance.email}&jfvfvjn={quote(make_password(otp_instance.temp_data['token']))}"
               send_otp_email(otp_instance.email, link, 'password_reset')
               messages.success(request, "A password reset link has been sent to your email. Follow the link to set a new password.")
               return render(request, 'forgetpassword.html', {'form': form, 'success': True})
        except Exception:  
            messages.error(request, "An error occurred, please try again after some time.")
    else:
        form = UserForgetPasswordForm()
    return render(request, 'forgetpassword.html', {'form': form, 'success': False})

def reset_password_view(request):
    email = request.GET.get('email')
    token = request.GET.get('jfvfvjn')
    if not email or not token:
        messages.error(request, "Invalid Request")
        return redirect('login')

    otp_obj = OTP.get_latest_valid(email, 'password_reset')
    if not otp_obj or not check_password(otp_obj.temp_data['token'], unquote(token)):
        messages.error(request, "Expired password reset link. Try again.")
        return redirect('forget_password')

    if request.method == 'POST':
        form = UserResetPasswordForm(request.POST)
        try:
            if form.is_valid():
                user = get_user_model().objects.get(email=email)
                if user.check_password(form.cleaned_data["new_password"]):
                    messages.error(request, "New password cannot be the same as the current password.")
                    return render (request, 'resetpassword.html', {'form': UserResetPasswordForm()})
                user.set_password(form.cleaned_data["new_password"])
                user.save()
                otp_obj.mark_verified()
                return render(request, 'resetpassword.html') #render a success message with login link. timer redirect
        except IntegrityError:
            messages.error(request, "An error occurred during password reset. Please try again after some time.")
    else:
        form = UserResetPasswordForm()
    return render(request, 'resetpassword.html', {'form': form})


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

