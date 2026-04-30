# booking/tests/conftest.py
import pytest
from datetime import date, timedelta
from django.contrib.auth import get_user_model
from rooms.models import Room
from booking.models import Booking

CustomUser = get_user_model()


@pytest.fixture
def user(db):
    """Создает пользователя для тестов booking"""
    return CustomUser.objects.create_user(
        username='booking_user',
        password='testpass123'
    )


@pytest.fixture
def room(db):
    """Создает комнату для тестов booking"""
    return Room.objects.create(
        number='101',
        room_type='standard',
        price_per_night=3000,
        capacity=2
    )


@pytest.fixture
def booking(db, user, room):
    """Создает бронь для тестов"""
    return Booking.objects.create(
        client=user,
        room=room,
        booking_date=date.today(),
        expiration_date=date.today() + timedelta(days=2),
        status='sleeping'
    )
