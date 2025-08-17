from django.urls import path
from problems.views import run_submit_view, ai_review_view

urlpatterns = [
    path('problem/<int:problem_id>/', run_submit_view, name='judge'),
    path('submission/<int:submission_id>/hint/', ai_review_view, name='ai_review'),
]