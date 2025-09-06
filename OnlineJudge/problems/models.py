from django.db import models
from django.contrib.auth.models import User

# A list of difficulty levels for problems.
DIFFICULTY_CHOICES = [
    ('Easy', 'Easy'),
    ('Medium', 'Medium'),
    ('Hard', 'Hard'),
]

# Create your models here.

class Languages(models.Model):
  
    name = models.CharField(
        max_length=50, 
        unique=True, 
        help_text="Full name of the language version(e.g., C++17, Python 3.9)"
    )
    
    extension = models.SlugField(
        max_length=50, 
        unique=True, 
        help_text="The file extension for this language (e.g., py, cpp)"
    )

    command = models.CharField(
        max_length=255,
        help_text="The command to execute the code. Use {source} and {executable} as placeholders."
    )

    class Meta:
      verbose_name = 'Programming Language'
      verbose_name_plural = 'Programming Languages'

    def __str__(self):
        return self.name


class Questions(models.Model):
   
    questionkey = models.CharField(max_length=100, blank=True, help_text="The UUID key ")

    title = models.CharField(max_length=255, help_text="The title of the problem.")
    description = models.TextField(help_text="A detailed description of the problem, including input/output format.")
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='Medium')
    
    # Execution constraints
    time_limit = models.FloatField(default=1.0, help_text="Time limit in seconds for a solution to run.")
    memory_limit = models.IntegerField(default=256, help_text="Memory limit in megabytes (MB).")

    # Meta information
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='authored_problems')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(default=False)

    class Meta:
      verbose_name = 'Question'
      verbose_name_plural = 'Questions'

    def __str__(self):
        return f"{self.title} ({self.difficulty})"


class TestCases(models.Model):
 
    problem = models.ForeignKey(Questions, on_delete=models.CASCADE, related_name='test_cases')
    input = models.TextField(help_text="The input for this test case.")
    expected_output = models.TextField(help_text="The expected output for this test case.")
    is_sample = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Test Case'
        verbose_name_plural = 'Test Cases'
        
    def __str__(self):
        sample_text = "Sample" if self.is_sample else "Hidden"
        return f"Test Case for '{self.problem.title}' ({sample_text})"



