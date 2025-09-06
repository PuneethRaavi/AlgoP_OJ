from django.db import models
from django.contrib.auth.models import User
from problems.models import Languages, Questions

# A list of possible statuses for a submission.
STATUS_CHOICES = [
    ('Pending', 'Pending'), # Default status (Debugging)
    ('Accepted', 'Accepted'),
    ('Wrong Answer', 'Wrong Answer'),
    ('Time Limit Exceeded', 'Time Limit Exceeded'),
    ('Syntax Error', 'Syntax Error'),
    ('Indentation Error', 'Indentation Error'),
    ('Value Error', 'Value Error'),
    ('Name Error', 'Name Error'),
    ('Type Error', 'Type Error'),
    ('Compilation Error', 'Compilation Error'),
    ('Runtime Error', 'Runtime Error'),
    ('System Error', 'System Error')
]

# Create your models here.

class Submissions(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')

    language = models.ForeignKey(Languages, on_delete=models.PROTECT, related_name='submissions', help_text="Language of the submission")
    problem = models.ForeignKey(Questions, on_delete=models.CASCADE, related_name='submissions', help_text="Problem Title")
    filekey = models.CharField(max_length=100, blank=True, help_text="The UUID key for code/input/output files.")
    
    # Execution results (filled in by the judge)  # Not functional as of now
    runtime = models.FloatField(null=True, blank=True, help_text="Execution time in seconds.")
    memory_used = models.IntegerField(null=True, blank=True, help_text="Memory used in megabytes (MB).")

    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Pending')
    submitted_at = models.DateTimeField(auto_now_add=True)

    output_log = models.TextField(blank=True, null=True) #For AI review, output is stored here for now
        
    def __str__(self):
        return f"{self.user.username} | {self.language.name} | {self.problem.title} [{self.status}] ({self.submitted_at:%Y-%m-%d %H:%M})"

    class Meta:
        ordering = ['-submitted_at']
        verbose_name = 'Submission'
        verbose_name_plural = 'Submissions'
