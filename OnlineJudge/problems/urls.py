from django.urls import path
from problems.views import run_submit_view

urlpatterns = [
    path('problem/<int:problem_id>/', run_submit_view, name='judge'),
]