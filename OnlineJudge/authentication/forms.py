from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from authentication.models import User

class UserRegistrationForm(UserCreationForm):
     class Meta:
        model = User
        fields = ("username", "first_name", "last_name","email", "password1", "password2")
    

class UserLoginForm(AuthenticationForm):
    pass
    
    
# class UserForgetPasswordForm(forms.Form):
#     username = forms.CharField()
#     password = forms.CharField(widget=forms.PasswordInput, label= "New Password")
#     confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm New Password")

#     def clean_username(self):
#         username = self.cleaned_data.get("username")

#         if not username:
#             raise forms.ValidationError("Username is required.")
#         try:
#             self.user = user_registrations.objects.get(username=username)
#         except user_registrations.DoesNotExist:
#             raise forms.ValidationError("Invalid username. Register first")

#         return username

#     def clean_password(self):
#         password = self.cleaned_data.get("password")
#         if 'username' in self.errors:
#             return password

#         if password and len(password) < 8:
#             raise forms.ValidationError("Password must be at least 8 characters long.")
#         if password and not re.search(r'\d', password):
#             raise forms.ValidationError("Password must contain at least one number.")
#         if password and not re.search(r'[^\w\s]', password):
#             raise forms.ValidationError("Password must contain at least one symbol.")

#         return password
    
#     def clean(self):
#         cleaned_data = super().clean()
#         password = cleaned_data.get("password")
#         confirm_password = cleaned_data.get("confirm_password")

#         if self.errors:
#             return cleaned_data
#         if password != confirm_password:
#             self.add_error('confirm_password', "Passwords do not match.")

#         if self.errors:
#             return cleaned_data
#         user = getattr(self, 'user', None)
#         if user and check_password(password, user.password):
#             raise forms.ValidationError( "New password cannot be the same as the old password.")

#         return cleaned_data
    
#     def save(self):
#         self.user.password = make_password(self.cleaned_data['password'])  
#         self.user.save()

    