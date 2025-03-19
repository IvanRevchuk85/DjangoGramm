import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def test_user(db):
    """Фикстура для создания тестового пользователя."""
    return User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="password123",
        first_name="Test",
        last_name="User",
        bio="This is a test bio",
        is_email_verified=True
    )


@pytest.fixture
def another_user(db):
    """Фикстура для создания второго тестового пользователя."""
    return User.objects.create_user(
        username="anotheruser",
        email="another@example.com",
        password="password456"
    )
