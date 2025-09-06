from django.shortcuts import render, redirect
from authentication.forms import UserRegistrationForm, UserLoginForm, UserForgetPasswordForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.db import IntegrityError
from authentication.decorators import SESSION_NEXT_KEY, if_authenticated_redirect


@if_authenticated_redirect
def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        try:
            if form.is_valid():
                form.save()     
                messages.success(request, "You've successfully registered. Please log in to continue.")
                return redirect('/login/')
            else:
                messages.error(request, "Please fix the errors below and resubmit.")
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
            login(request, form.user)
            next_url = request.session.pop(SESSION_NEXT_KEY, '/')
            return redirect(next_url)
    else:
        form = UserLoginForm()
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
    logout(request)
    messages.success(request, "You've been logged out successfully.")
    return redirect('/login/')