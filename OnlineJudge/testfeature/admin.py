from django.contrib import admin
from testfeature.models import userlog
from testfeature.forms import UserForm
# Register your models here.
class UserLogAdmin(admin.ModelAdmin):
    form = UserForm
    list_display = ('user_id', 'timestamp','password')  # Display user_id and timestamp in the admin interface
admin.site.register(userlog, UserLogAdmin)  