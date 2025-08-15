from django.contrib import admin
from problems.models import Submissions, Languages, Questions, TestCases
from problems.forms import QuestionAdminForm
from problems.utils import save_testcases


# This allows editing TestCases directly within the Problem admin page
class TestCaseInline(admin.TabularInline):
    model = TestCases
    extra = 1  # Show 1 extra empty form for a new test case
    
    fields = ('input', 'expected_output', 'is_sample')


# This customizes the admin interface for the Problems model
@admin.register(Questions)
class QuestionAdmin(admin.ModelAdmin):
    form = QuestionAdminForm
    
    list_display = ('id', 'title', 'difficulty','questionkey')
    list_display_links = ('id', 'title')
    readonly_fields = ('questionkey',)
    search_fields = ('title',)
    inlines = [TestCaseInline] # Attach the TestCase editor

    def save_model(self, request, obj, form, change):
        # First, save the Question object itself. This is important to ensure it has an ID before we proceed.
        super().save_model(request, obj, form, change)

        # Get the uploaded files from the form's cleaned data
        input_file = form.cleaned_data.get('main_input_file')
        output_file = form.cleaned_data.get('main_output_file')

        # Proceed only if both files have been uploaded
        if input_file and output_file:
            save_testcases(obj, input_file, output_file)
            

# Customize the admin interface for Languages
@admin.register(Languages)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'extension', 'command')
    search_fields = ('name', 'extension')


# Display Test Cases in Admin Panel
admin.site.register(TestCases)


# Register the Submissions model with a basic interface
@admin.register(Submissions)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'language', 'status', 'filekey', 'submitted_at')
    list_filter = ('status', 'language')
    search_fields = ('user__username',) # Search by username
    readonly_fields = ('submitted_at','filekey') # Make timestamp read-only

