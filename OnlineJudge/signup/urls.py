from django.urls import path
from signup.views import homepage_view, register_view
# from testfeature.views import user_log_view, user_details

urlpatterns = [
    path('home/',homepage_view, name='homepage'),  # URL for user details
    path('register/', register_view, name='register') # URL for user registration
]