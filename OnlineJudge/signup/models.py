from django.db import models

# Create your models here.
class user_registrations (models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)

    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    confirm_password = models.CharField(max_length=255)

    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Registration'
        verbose_name_plural = 'Registrations'

    def __str__(self):
        return f"{self.username} ({self.email})-{self.password}"