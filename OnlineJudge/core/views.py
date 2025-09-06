from django.shortcuts import render
from submissions.models import Submissions, STATUS_CHOICES
from problems.models import Questions, DIFFICULTY_CHOICES
from authentication.decorators import session_check_proceed, public_page_context
from problems.forms import CompilerForm
from problems.views import execute_code
from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Q
from pathlib import Path
import uuid, os

# Create your views here.

@session_check_proceed
def wip_view(request):
    user=request.user
    context={'user':user}
    return render(request, 'wip.html', context)



@public_page_context
def home_view(request, context):
    return render(request, 'home.html', context)  



@public_page_context
def problems_view(request, context):
    questions = Questions.objects.all()

    # Search across title and author
    search_query = request.GET.get('q', '').strip()
    if search_query:
        questions = questions.filter(
            Q(title__icontains=search_query) |
            Q(author__username__icontains=search_query)
        )

    # Difficulty filter
    difficulty = request.GET.get('difficulty', 'All')
    if difficulty and difficulty != 'All':
        questions = questions.filter(difficulty=difficulty)

    # Sorting
    sort = request.GET.get('sort', 'date')
    dir = request.GET.get('dir', 'desc')
    sort_fields={
        'title': 'title',
        'date': 'created_at'
    }
    sort_field = sort_fields.get(sort, 'created_at')
    if dir == 'asc':
        questions = questions.order_by(sort_field)
    else:
        questions = questions.order_by(f'-{sort_field}')

    # Pagination
    paginator = Paginator(questions, 7)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context['questions'] = page_obj
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

            submissions_dir = Path(settings.BASE_DIR) / "submissions" / "files"
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
    user_submissions = Submissions.objects.filter(user=user).select_related('problem', 'language')

    # Filter selections (lists)
    difficulties = [d for d in request.GET.getlist('difficulty') if d]
    if difficulties:
        user_submissions = user_submissions.filter(problem__difficulty__in=difficulties)
    status = [s for s in request.GET.getlist('status') if s]
    if status:
        user_submissions = user_submissions.filter(status__in=status)
    languages = [l for l in request.GET.getlist('language') if l]
    if languages:
        user_submissions = user_submissions.filter(language__name__in=languages)

    # Choices 
    difficulty_choices = [value for value, _ in DIFFICULTY_CHOICES]
    status_choices = [value for value, _ in STATUS_CHOICES]
    language_choices = list(Submissions.objects.filter(user=user).values_list('language__name', flat=True).distinct().order_by('language__name'))
    
    # Search across problem title, status, language name
    search_query = request.GET.get('q', '').strip()
    if search_query:
        user_submissions = user_submissions.filter(
            Q(problem__title__icontains=search_query) |
            Q(status__icontains=search_query) |
            Q(language__name__icontains=search_query)
        )

    # Sorting
    sort = request.GET.get('sort', 'submitted')
    dir = request.GET.get('dir', 'desc')
    sort_fields = {
        'title': 'problem__title',
        'submitted': 'submitted_at',
    }
    sort_field = sort_fields.get(sort, 'submitted_at')
    if dir == 'asc':
        user_submissions = user_submissions.order_by(sort_field)
    else:
        user_submissions = user_submissions.order_by(f'-{sort_field}')

    # Pagination
    paginator = Paginator(user_submissions, 7)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'submissions': page_obj,
        'difficulty_choices': difficulty_choices,
        'status_choices': status_choices,
        'language_choices': language_choices,
        'selected_difficulties': difficulties,
        'selected_statuses': status,
        'selected_languages': languages,
    }
    return render(request, 'submissions.html', context)


# @session_check_proceed
# def upload_view(request):
#     pass