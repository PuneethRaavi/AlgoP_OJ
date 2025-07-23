from django.db import models

# Create your models here.
class userlog(models.Model):
    user_id = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    def __str__(self):
        return f"{self.user_id}"