from django.shortcuts import render, redirect
from signup.forms import UserRegistrationForm
from django.contrib import messages
# from django.views.decorators.csrf import csrf_exempt #test attack
# Create your views here.
def homepage_view(request):
    return render(request, 'homepage.html')  # automatically handles template and context without loader and httpresponse 

# @csrf_exempt  # test attack
def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/home/')
        else:
            messages.error(request, "Try again")
    else:
        form = UserRegistrationForm()
    return render(request, 'signuppage.html', {'form': form})