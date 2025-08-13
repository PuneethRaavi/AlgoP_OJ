from django import forms
from problems.models import Languages, Questions

class CompilerForm(forms.Form):
    # We explicitly define the language field to use a ModelChoiceField, which will render as a <select> dropdown in the template.
    language = forms.ModelChoiceField(
        queryset=Languages.objects.all(),
        empty_label=None,
        widget=forms.Select(attrs={
            'class': 'mt-1 block w-full max-w-xs px-2 py-1.5 text-sm bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-slate-100 dark:focus:ring-gray-600 focus:border-slate-200 dark:focus:border-gray-500 transition duration-300'
        }),
        label="Language",
    )

    theme = forms.ChoiceField(
        choices= [
            ('dracula', 'Dracula'),
            ('material', 'Material'),
            ('monokai', 'Monokai'),
            ('cobalt', 'Cobalt'),
            ('eclipse', 'Eclipse'),
        ],
        widget=forms.Select(attrs={
            'class': 'mt-1 block w-full max-w-xs px-2 py-1.5 text-sm bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-slate-100 dark:focus:ring-gray-600 focus:border-slate-200 dark:focus:border-gray-500 transition duration-300'        
        }),
        label="Theme",
    )

    code = forms.CharField(
        widget=forms.Textarea(attrs={     
            'rows': 15,
            'placeholder': 'Write your code here...'
        }),
        label="Code Here! "
    ) 

    input = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 2,
            'placeholder': 'Provide input for your code here...'
        }),
        required=False,
        label="Input"
    )
    
  
class QuestionAdminForm(forms.ModelForm):
  
    main_input_file = forms.FileField(
        label="Main Input File", 
        help_text="Upload the complete input data file for all hidden test cases.",
        required=False # Optional, so you can create a problem without test files first.
    )
    main_output_file = forms.FileField(
        label="Main Output File", 
        help_text="Upload the corresponding complete output data file.",
        required=False
    )

    class Meta:
        model = Questions
        fields = '__all__' # Include all fields from the Questions model
