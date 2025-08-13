from django.shortcuts import render
from problems.models import Questions, user_registrations
from authentication.decorators import session_check_proceed, public_page_context

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



@session_check_proceed  # Ensures user is logged in before accessing submissions
def submissions_view(request):
    user = request.user
    
    context = {
        'user': user
    }
    return render(request, 'submissions.html', context)  # automatically handles template and context without loader and httpresponse 
