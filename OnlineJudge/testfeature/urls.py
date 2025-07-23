from django.urls import path
from testfeature.views import user_log_view, user_details

urlpatterns = [
    path('',user_log_view,name="7"),  # Include authentication app URLs
    path('<str:id>/', user_details, name='user_details')  # URL for user details
]