import pytest
from users.forms import CustomUserCreationForm, EditProfileForm
from users.models import CustomUser
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.mark.django_db
def test_valid_user_creation_form():
    """Тестирует создание нового пользователя через форму."""
    form_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password1": "StrongPass123!",
        "password2": "StrongPass123!",
    }
    form = CustomUserCreationForm(data=form_data)
    assert form.is_valid(), form.errors


@pytest.mark.django_db
def test_duplicate_email(test_user):
    """Тестирует, что нельзя зарегистрировать двух пользователей с одинаковым email."""
    form_data = {
        "username": "user2",
        "email": "test@example.com",
        "password1": "AnotherPass123!",
        "password2": "AnotherPass123!",
    }
    form = CustomUserCreationForm(data=form_data)
    assert not form.is_valid()
    assert "email" in form.errors


@pytest.mark.django_db
def test_password_mismatch():
    """Тестирует, что форма не принимает несовпадающие пароли."""
    form_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password1": "StrongPass123!",
        "password2": "WrongPass123!",
    }
    form = CustomUserCreationForm(data=form_data)
    assert not form.is_valid()
    assert "password2" in form.errors


@pytest.mark.django_db
def test_edit_profile_valid(test_user):
    """Тестирует успешное редактирование профиля."""
    form_data = {
        "first_name": "Updated",
        "last_name": "Name",
        "bio": "Updated bio"}
    form = EditProfileForm(instance=test_user, data=form_data)
    assert form.is_valid(), form.errors
    form.save()

    test_user.refresh_from_db()
    assert test_user.get_full_name() == "Updated Name"
    assert test_user.bio == "Updated bio"


@pytest.mark.django_db
def test_edit_profile_avatar_size(test_user):
    """Тестирует ограничение на размер загружаемого аватара(>2MB)"""
    large_avatar = SimpleUploadedFile(
        "large.jpg", b"1" * (2 * 1024 * 1024 + 1), content_type="image/jpeg")
    form = EditProfileForm(instance=test_user, data={}, files={
                           "avatar": large_avatar})
    assert not form.is_valid()
    assert "avatar" in form.errors
