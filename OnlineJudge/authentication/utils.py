from django.core.mail import send_mail
from django.conf import settings


def send_otp_email(email: str, otp: str, purpose: str = "registration") -> None:
    if purpose == "password_reset":
        subject = f"Password Reset Link for OnlineJudge"
        message = (
            f"Hello,\n\n"
            f"To reset your password, please click the link below:\n"
            f"{otp}\n\n"
            f"This link will expire shortly. If you did not request this, you can ignore this email.\n\n"
            f"Regards,\nOnlineJudge Team"
        )
    else:
        subject = f"Your OTP for {purpose.capitalize()}"
        message = (
            f"Hello,\n\n"
            f"Your One-Time Password (OTP) for {purpose} is: {otp}\n"
            f"This code will expire shortly. If you did not request this, you can ignore this email.\n\n"
            f"Regards,\nOnlineJudge Team"
    )
    send_mail(
        subject=subject,
        message=message,
        from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', None),
        recipient_list=[email],
        fail_silently=True,  # Avoid breaking flow if email backend has a transient issue
    )
