from django.contrib import admin
from authentication.models import OTP

# Register your models here.

@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ('email', 'purpose', 'otp', 'is_verified', 'created_at', 'expires_at')
    list_filter = ('purpose', 'is_verified')
    search_fields = ('email', 'otp')
    readonly_fields = ('created_at', 'expires_at')
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return True
