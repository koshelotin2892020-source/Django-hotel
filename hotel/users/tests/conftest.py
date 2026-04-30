# users/tests/conftest.py
import pytest
from datetime import date
from django.contrib.auth import get_user_model
from users.models import AccountInfo

CustomUser = get_user_model()


@pytest.fixture
def user(db):
    """Создает пользователя для тестов users"""
    return CustomUser.objects.create_user(
        username='testuser',
        password='testpass123'
    )


@pytest.fixture
def another_user(db):
    """Создает другого пользователя для тестов уникальности"""
    return CustomUser.objects.create_user(
        username='another_user',
        password='testpass123'
    )


@pytest.fixture
def account_info(db, user):
    """Создает профиль с валидными данными"""
    return AccountInfo.objects.create(
        account=user,
        first_name='Иван',
        last_name='Петров',
        phone='+7 123 456-78-90',
        email='ivan@gmail.com',
        birthday=date(1990, 1, 1)
    )
