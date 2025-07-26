from django.contrib import admin
from authentication.models import user_registrations
from authentication.forms import UserRegistrationForm

# Register your models here.
class UserRegistrationAdmin(admin.ModelAdmin):
    form = UserRegistrationForm
    list_display = ('first_name', 'last_name', 'email', 'username','password', 'timestamp')
    search_fields = ('first_name', 'last_name', 'email', 'username')
admin.site.register(user_registrations,UserRegistrationAdmin)
