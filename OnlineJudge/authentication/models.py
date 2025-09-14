from django.db import models
from django.utils import timezone
from datetime import timedelta

PURPOSE_CHOICES = [
    ('registration', 'Registration'),
    ('password_reset', 'Password Reset'),
    ('password_change', 'Password Change'),
]

# Using Django's inbuilt User model for authentication

class OTP(models.Model):

    email = models.EmailField(help_text="Email address for OTP verification")
    purpose = models.CharField(max_length=20, choices=PURPOSE_CHOICES, help_text="Purpose of OTP")
    otp = models.CharField(max_length=6, help_text="6-digit OTP code")
    temp_data = models.JSONField(default=dict, blank=True, help_text="Temporary data storage")

    is_verified = models.BooleanField(default=False, help_text="Whether OTP has been verified")
    created_at = models.DateTimeField(auto_now_add=True, help_text="OTP creation time")
    expires_at = models.DateTimeField(help_text="OTP expiration time")
    
    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=15)
        super().save(*args, **kwargs)
    
    class Meta:
        db_table = 'Auth_Otp'
        ordering = ['-created_at']
        verbose_name = 'OTP Verification'
        verbose_name_plural = 'OTP Verifications'
        indexes = [
            models.Index(fields=['email', 'purpose', 'is_verified', '-created_at']),
        ]

    @classmethod
    def get_latest_valid(cls, email, purpose):
        otp = cls.objects.filter(
            email=email,
            purpose=purpose,
            is_verified=False
        ).order_by('-created_at').first()
        return otp if otp and otp.expires_at > timezone.now() else None

    def mark_verified(self):
        self.is_verified = True
        self.save(update_fields=["is_verified"])

    def __str__(self):
        purpose_display = dict(PURPOSE_CHOICES).get(self.purpose, self.purpose)
        status = 'Verified' if self.is_verified else 'Pending'
        return f"{self.email} - {purpose_display} ({status})"