import pytest
from django.urls import reverse
from users.models import CustomUser


@pytest.mark.django_db
def test_register_view(client):
    """Тест успешной регистрации пользователя."""
    response = client.post(reverse('users:register'), {
        "username": "testuser",
        "email": "test@example.com",
        "password1": "TestPass123!",
        "password2": "TestPass123!",
    })
    assert response.status_code == 302  # Перенаправление после успешной регистрации
    assert CustomUser.objects.filter(email="test@example.com").exists()


@pytest.mark.django_db
def test_register_duplicate_email(client, test_user):
    """Тест регистрации с уже существующим email (ошибка)."""
    response = client.post(reverse('users:register'), {
        "username": "user2",
        "email": "test@example.com",
        "password1": "AnotherPass123!",
        "password2": "AnotherPass123!",
    })
    # Ошибка должна отобразиться на той же странице
    assert response.status_code == 200
    assert "Пользователь с таким email уже существует." in response.content.decode()


@pytest.mark.django_db
def test_confirm_email(client, test_user):
    """Тест подтверждения email."""
    test_user.is_email_verified = False
    test_user.save()
    response = client.get(reverse('users:confirm_email',
                          kwargs={'user_id': test_user.id}))
    test_user.refresh_from_db()
    assert test_user.is_email_verified is True
    assert response.status_code == 302  # Перенаправление после подтверждения


@pytest.mark.django_db
def test_login_view(client, test_user):
    """Тест успешного входа в систему."""
    response = client.post(reverse('users:login'), {
        "username": "testuser",
        "password": "password123",
    })
    assert response.status_code == 302  # Перенаправление после входа


@pytest.mark.django_db
def test_login_invalid_password(client, test_user):
    """Тест входа с неверным паролем (ошибка)."""
    response = client.post(reverse('users:login'), {
        "username": "testuser",
        "password": "wrongpassword",
    })
    assert response.status_code == 200
    assert "Неверные данные для входа." in response.content.decode()


@pytest.mark.django_db
def test_profile_view(client, test_user):
    """Тест доступа к профилю (только для авторизованных пользователей)."""
    client.force_login(test_user)
    response = client.get(reverse('users:profile'))
    # Страница достурна авторизованному пользователю
    assert response.status_code == 200


@pytest.mark.django_db
def test_edit_profile(client, test_user):
    """Тест успешного редактирования профиля."""
    client.force_login(test_user)
    response = client.post(reverse('users:edit_profile'), {
        "first_name": "Updated",
        "last_name": "Name",
        "bio": "Updated bio",
    })
    test_user.refresh_from_db()
    assert test_user.get_full_name().strip() == "Updated Name"
    assert test_user.bio == "Updated bio"
    assert response.status_code == 302  # Перенаправление после обновления профиля
