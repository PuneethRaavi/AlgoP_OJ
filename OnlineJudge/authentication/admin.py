from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from authentication.models import User    

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('id', 'email', 'username', 'first_name','last_name','is_staff', 'is_active')
   
