from django.urls import path
from authentication import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('verify/', views.verify_registration, name='verify_registration'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('forget-password/', views.forget_password_view, name='forget_password'),
    path('reset-password/', views.reset_password_view, name='reset_password'),

    path('google/login/', views.google_login_view, name='google_login'),
    path('google/callback/', views.google_callback_view, name='google_callback'),
    path('github/login/', views.github_login_view, name='github_login'),
    path('github/callback/', views.github_callback_view, name='github_callback'),
]