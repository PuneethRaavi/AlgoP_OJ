from django import forms
from problems.models import Languages, Questions

class CompilerForm(forms.Form):
    # We explicitly define the language field to use a ModelChoiceField, which will render as a <select> dropdown in the template.
    language = forms.ModelChoiceField(
        queryset=Languages.objects.all(),
        empty_label=None,
        widget=forms.Select(attrs={
            'class': 'mt-1 block w-full max-w-xs px-1.5 py-1 text-[10px] dark:text-stone-400 bg-white dark:bg-slate-800 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-slate-100 dark:focus:ring-gray-600 focus:border-slate-200 dark:focus:border-gray-500 transition duration-300'
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
            'class': 'mt-1 block w-full max-w-xs px-1.5 py-1 text-[10px] dark:text-stone-400 bg-white dark:bg-slate-800 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-slate-100 dark:focus:ring-gray-600 focus:border-slate-200 dark:focus:border-gray-500 transition duration-300'        
        }),
        label="Theme",
    )

    fontSize = forms.ChoiceField(
        choices=[
            ('8px' , '8px' ),
            ('10px', '10px'),
            ('12px', '12px'),
            ('14px', '14px'),
        ],
        widget=forms.Select(attrs={
            'class': 'appearance-none block w-full max-w-xs px-1 py-1 text-[9px] dark:text-stone-400 bg-white dark:bg-slate-800 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-slate-100 dark:focus:ring-gray-600 focus:border-slate-200 dark:focus:border-gray-500 transition duration-300'
        }),
        initial='12px' 
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
            'rows': 5,
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


#Question upload form, multiple sample cases upload issue as of now- getting complex