from django.urls import path
from authentication.views import dashboard_view

urlpatterns = [
    path('dashboard/',dashboard_view, name='dashboard'),  # URL for dashboard view
    
]

