from django import forms
from authentication.models import user_registrations
from django.contrib.auth.hashers import make_password, check_password
import re

class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = user_registrations
        fields = ['first_name', 'last_name', 'email', 'username', 'password', 'confirm_password']
        widgets = {
            'password': forms.PasswordInput(),
            'confirm_password': forms.PasswordInput(),
        }
    
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
            # attach error to a field instead of raising non-field error
            self.add_error('confirm_password', "Passwords do not match.")

        return cleaned_data

    
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.password = make_password(self.cleaned_data["password"])
        if commit:
            instance.save()
        return instance
   

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get("username")

        if not username:
            raise forms.ValidationError("Username is required.")
        try:
            self.user = user_registrations.objects.get(username=username)
        except user_registrations.DoesNotExist:
            raise forms.ValidationError("Invalid username. Please register first or try again.")

        return username

    def clean_password(self):
        password = self.cleaned_data.get("password")

        # If username already has an error, skip password validation
        if 'username' in self.errors:
            return password  # return without validating

        if not password:
            raise forms.ValidationError("Password is required.")

        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")

        # If username does not exist, skip password validation
        if self.errors:
            return cleaned_data

        user = getattr(self, 'user', None)

        if user and not check_password(password, user.password):
            self.add_error('password', "Invalid password.")

        return cleaned_data