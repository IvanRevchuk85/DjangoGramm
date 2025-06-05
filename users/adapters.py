from allauth.account.models import EmailAddress
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class NoEmailVerificationSocialAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request, sociallogin):
        return True

    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        # We immediately confirm the email from the social network
        if sociallogin.email_addresses:
            for email_address in sociallogin.email_addresses:
                email_address.user = user
                email_address.verified = True

                # Check: does such user+email combination already exist?
                exists = EmailAddress.objects.filter(
                    user=user, email=email_address.email).exists()
                if not exists:
                    email_address.save()
        return user
