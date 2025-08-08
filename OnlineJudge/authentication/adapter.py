from allauth.exceptions import ImmediateHttpResponse
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.models import EmailAddress
from django.shortcuts import redirect

# class MySocialAccountAdapter(DefaultSocialAccountAdapter):

#     def pre_social_login(self, request, sociallogin):
#         """
#         Invoked just after a user successfully authenticates via a
#         social provider, but before the login is actually processed
#         (and before any local user account is created/retrieved).
#         """
#         # The user is already logged in, so we're just connecting a new social account.
#         if request.user.is_authenticated:
#             return

#         # The social account is already connected to a user.
#         if sociallogin.is_existing:
#             return

#         # Check if an account already exists with this email address.
#         try:
#             # Find an existing EmailAddress object
#             email_address = EmailAddress.objects.get(email__iexact=sociallogin.user.email)

#             # If the email is associated with a user, connect the social login to that user.
#             user = email_address.user
#             sociallogin.connect(request, user)
            
#             # The original flow would show a confirmation page, 
#             # but we can bypass that and log the user in directly.
#             # This raises an exception that is caught by allauth to redirect.
#             raise ImmediateHttpResponse(redirect('/dashboard/')) # Or any other success URL

#         except EmailAddress.DoesNotExist:
#             # No account with this email, so continue with the normal signup process.
#             pass