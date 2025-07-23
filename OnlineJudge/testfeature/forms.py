from django import forms
from testfeature.models import userlog
from django.contrib.auth.hashers import make_password

# Create your forms here.
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = userlog
        fields = ['user_id', 'password']

    def save(self, commit = ...):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user  