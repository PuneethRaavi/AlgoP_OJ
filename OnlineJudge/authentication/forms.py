from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
import re

class UserRegistrationForm(forms.ModelForm):

    username = forms.CharField()
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("A user with this username already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if password and len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        if password and not re.search(r'\d', password):
            raise forms.ValidationError("Password must contain at least one number.")
        if password and not re.search(r'[^\w\s]', password):
            raise forms.ValidationError("Password must contain at least one symbol.")
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.") # Attach error to a field instead of raising non-field error
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.set_password(self.cleaned_data["password"])
        if commit:
            instance.save()
        return instance
   

class UserLoginForm(forms.Form):
    username = forms.CharField(error_messages={'required': 'Username is required.'})
    password = forms.CharField(widget=forms.PasswordInput, error_messages={'required': 'Password is required.'})

    def clean_username(self):
        username = self.cleaned_data.get("username")
        try:
            self.user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError("Invalid username. Please register first or try again.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        user = getattr(self, 'user', None)
        if user and password and not user.check_password(password):
            self.add_error('password', "Invalid password.")
        return cleaned_data
    
    
class UserForgetPasswordForm(forms.Form):
    email = forms.CharField()
    # password = forms.CharField(widget=forms.PasswordInput, label= "New Password")
    # confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm New Password")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        # if not email:
        #     raise forms.ValidationError("Email is required.")
        try:
            self.user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError("Invalid Email ID. Register first")
        return email

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if password and len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        if password and not re.search(r'\d', password):
            raise forms.ValidationError("Password must contain at least one number.")
        if password and not re.search(r'[^\w\s]', password):
            raise forms.ValidationError("Password must contain at least one symbol.")
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
            return cleaned_data
        if self.user and check_password(password, self.user.password):
            raise forms.ValidationError("New password cannot be the same as the old password.")
        return cleaned_data

    def save(self):
        self.user.password = make_password(self.cleaned_data['password'])
        self.user.save()
