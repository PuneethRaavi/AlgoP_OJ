from django import forms
from signup.models import user_registrations
from django.contrib.auth.hashers import make_password
import re

class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = user_registrations
        fields = ['first_name', 'last_name', 'email', 'username', 'password', 'confirm_password']
        widgets = {
            'password': forms.PasswordInput(),
            'confirm_password': forms.PasswordInput(),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        
        # Password match check
        if password != confirm_password:
            raise forms.ValidationError("Passwords should match.")

        # Password length check
        if password and len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")

        # At least one number
        if password and not re.search(r'\d', password):
            raise forms.ValidationError("Password must contain at least one number.")

        # At least one symbol
        if password and not re.search(r'[^\w\s]', password):
            raise forms.ValidationError("Password must contain at least one symbol.")

        return cleaned_data

    
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.password = make_password(self.cleaned_data["password"])
        if commit:
            instance.save()
        return instance