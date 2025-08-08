from django.urls import path
from authentication.views import dashboard_view, register_view, login_view, logout_view, forget_password_view, home_view

urlpatterns = [
    path('', home_view, name='home'),  # Home Page
    path('dashboard/',dashboard_view, name='dashboard'),  # URL for dashboard view
    path('register/', register_view, name='register'), # URL for user registration view
    path('forgetpassword/', forget_password_view, name='forget_password'),  # URL for password reset view
    path('login/', login_view, name='login'),  # URL for user login view
    path('logout/', logout_view, name='logout')
]