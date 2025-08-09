from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from authentication.forms import UserRegistrationForm, UserLoginForm
from django.contrib import messages
from django.db import IntegrityError
# from django.views.decorators.csrf import csrf_exempt #test attack

# Create your views here.
def home_view(request):
    return render(request, 'homepage.html')

@login_required
def dashboard_view(request):
    user = request.user
    context = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'username': user.username,
    }
    return render(request, 'dashboard.html', context)  # automatically handles template and context without loader and httpresponse 

# @csrf_exempt  # test attack
def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        try:
            if form.is_valid():
                form.save() #database violatation will be handled by form validation
                messages.success(request, "You've successfully registered. Please log in to continue.")
                return redirect('/login/')
            else:
                messages.error(request, "Please fix the errors below and resubmit.")
                #inbuilt - form with validation errors will be displayed in the template
        except IntegrityError:
                 messages.error(request, "A user with that username already exists. Please choose a different one.")
                 #Same time same username register error
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()  
            login(request, user) # ✨ Use Django's login function
            messages.success(request, "You've successfully logged in.")
            return redirect("/dashboard/") #customise to redirect to request site
    else:
        form = UserLoginForm()

    return render(request, "login.html", {"form": form})


# def forget_password_view(request):
#     if request.method == 'POST':
#         form = UserForgetPasswordForm(request.POST)
#         if form.is_valid():
#            form.save() #database violatation will be handled by form validation
#            messages.success(request, "You've successfully changed password. Please log in to continue.")
#            return redirect('/login/')
#         # else:
#         #    #inbuilt - form with validation errors will be displayed in the template
#     else:
#         form = UserForgetPasswordForm()

#     return render(request, 'forgetpassword.html', {'form': form})

    
def logout_view(request):
    logout(request) 
    messages.success(request, "You've been logged out successfully.")
    return redirect('/login/')