from django.contrib import admin
from submissions.models import Submissions

# Register your models here.

# Register the Submissions model with a basic interface
@admin.register(Submissions)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'language', 'status', 'filekey', 'submitted_at')
    list_filter = ('status', 'language')
    search_fields = ('user__username',) # Search by username
    readonly_fields = ('submitted_at','filekey') # Make timestamp read-only