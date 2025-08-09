from django.urls import path
from authentication.views import dashboard_view, register_view, login_view, logout_view, home_view #, forget_password_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home_view, name='home'),  # Home Page
    path('dashboard/',dashboard_view, name='dashboard'),  # URL for dashboard view
    path('register/', register_view, name='register'), # URL for user registration view
    path('forgetpassword/', auth_views.PasswordResetView.as_view(), name='forget_password'),  # URL for password reset view
    path('login/', login_view, name='login'),  # URL for user login view
    path('logout/', logout_view, name='logout')
]