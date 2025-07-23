from django.shortcuts import render 
from testfeature.models import userlog
from django.http import HttpResponse
from django.template import loader
# Create your views here.

def user_log_view(request):
    student_logs = userlog.objects.all()  # Fetch all user logs
    template = loader.get_template('userlog.html')  # Load the template 
    context = {
        'student_logs': student_logs,  # Pass the logs to the template
    }
    return HttpResponse(template.render(context, request))  # Render the template with context

def user_details(request, id):
   student_details = userlog.objects.get(id=id)  # Fetch user details by user_id
   template = loader.get_template('user_details.html')  # Load the user details template
   context = {
       'student': student_details,  # Pass the user details to the template
   }
   return HttpResponse(template.render(context, request))  # Render the template with context