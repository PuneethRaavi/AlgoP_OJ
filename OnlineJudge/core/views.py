from django.shortcuts import render
from problems.models import Questions, Submissions
from authentication.decorators import session_check_proceed, public_page_context
from problems.forms import CompilerForm
from problems.views import execute_code
from django.conf import settings
import uuid, os
from pathlib import Path

# Create your views here.

@public_page_context
def home_view(request, context):
    return render(request, 'home.html', context)  



# @session_check_proceed
@public_page_context
def wip_view(request, context):
    return render(request, 'wip.html', context)



@public_page_context
def problems_view(request, context):
    all_questions = Questions.objects.all()
    context.update ({
        'questions': all_questions,
    })       
    return render(request, 'problems.html', context)

 

@public_page_context
def compiler_view(request, context):
    user = context['user']
    if request.method == 'POST':
        form = CompilerForm(request.POST)
        if form.is_valid():
            language = form.cleaned_data['language']
            code = form.cleaned_data['code']
            input = form.cleaned_data['input']
            
            filekey = str(uuid.uuid4())

            submissions_dir = Path(settings.BASE_DIR) / "submissions"
            codes_dir = submissions_dir / "codes"
            inputs_dir = submissions_dir / "inputs"
            outputs_dir = submissions_dir / "outputs"
            
            code_file_path = codes_dir / f"{filekey}.{language.extension}"
            input_file_path = inputs_dir / f"{filekey}.txt"
            output_file_path = outputs_dir / f"{filekey}.txt"
            executable_path = codes_dir / filekey

            try:
                status, output,_ = execute_code(language, code, input, filekey)
                context = {'form': form, 'status': status, 'output': output, 'user':user}
                return render(request, 'compiler.html', context)
            finally:
                for path in [code_file_path, input_file_path, output_file_path, executable_path]:
                    if path.exists():
                        os.remove(path)
    
    form = CompilerForm()
    context = {'form': form, 'status': None, 'output': 'Your output will appear here...', 'user':user}

    return render(request, 'compiler.html', context)



@session_check_proceed  
def submissions_view(request):
    user = request.user
    user_submissions = Submissions.objects.filter(user=user).select_related('problem', 'language').order_by('-submitted_at')

    context={
        'submissions': user_submissions,
    }
    
    return render(request, 'submissions.html', context)


# @session_check_proceed
# def upload_view(request):
#     pass