from django.urls import path
from authentication.views import register_view, login_view, logout_view, forget_password_view, google_login_view, google_callback_view, github_login_view, github_callback_view

urlpatterns = [
    path('register/', register_view, name='register'), # URL for user registration view
    path('forgetpassword/', forget_password_view, name='forget_password'),  # URL for password reset view
    path('login/', login_view, name='login'),  # URL for user login view
    path('logout/', logout_view, name='logout'),

    path('google/login/', google_login_view, name='google_login'),
    path('google/callback/', google_callback_view, name='google_callback'),
    path('github/login/', github_login_view, name='github_login'),
    path('github/callback/', github_callback_view, name='github_callback'),
]