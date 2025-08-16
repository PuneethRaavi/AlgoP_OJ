from django.db import models
from authentication.models import user_registrations
from problems.models import Languages, Questions, STATUS_CHOICES

# Create your models here.

class Submissions(models.Model):

    user = models.ForeignKey(user_registrations, on_delete=models.CASCADE, related_name='submissions')

    language = models.ForeignKey(Languages, on_delete=models.PROTECT, related_name='submissions', help_text="Language of the submission")
    problem = models.ForeignKey(Questions, on_delete=models.CASCADE, related_name='submissions', help_text="Problem Title")
    filekey = models.CharField(max_length=100, blank=True, help_text="The UUID key for code/input/output files.")
    
    # Execution results (filled in by the judge)  # Not functional as of now
    runtime = models.FloatField(null=True, blank=True, help_text="Execution time in seconds.")
    memory_used = models.IntegerField(null=True, blank=True, help_text="Memory used in megabytes (MB).")

    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Pending')
    submitted_at = models.DateTimeField(auto_now_add=True)
        
    def __str__(self):
        return f"{self.user.username} | {self.language.name} | {self.problem.title} [{self.status}] ({self.submitted_at:%Y-%m-%d %H:%M})"

    class Meta:
        ordering = ['-submitted_at']
        verbose_name = 'Submission'
        verbose_name_plural = 'Submissions'
