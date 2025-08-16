from django.urls import path
from submissions.views import submission_detail_view

urlpatterns = [
    path('submission/<str:filekey>/', submission_detail_view, name='submission_detail'),
]