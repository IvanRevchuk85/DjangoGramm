import pytest
from django.test import RequestFactory
from allauth.account.models import EmailAddress
from users.models import CustomUser
from users.adapters import NoEmailVerificationSocialAdapter

@pytest.mark.django_db
def test_save_user_sets_verified_email():
    user = CustomUser.objects.create(email="ivan@example.com")
    factory = RequestFactory()
    request = factory.get("/")

    adapter = NoEmailVerificationSocialAdapter()

    class DummyEmail:
        def __init__(self, email):
            self.email = email
            self.user = None
            self.verified = False

        def save(self):
            EmailAddress.objects.create(user=self.user, email=self.email, verified=self.verified)

    email_obj = DummyEmail("ivan@example.com")

    class DummySocialLogin:
        def __init__(self):
            self.email_addresses = [email_obj]
            self.user = user
        def save(self, request):
            pass


    sociallogin = DummySocialLogin()

    result_user = adapter.save_user(request, sociallogin, form=None)

    email_record = EmailAddress.objects.get(email="ivan@example.com")

    assert result_user == user
    assert email_record.verified is True
    assert email_record.user == user
