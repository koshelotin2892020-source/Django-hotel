# rooms/tests/conftest.py
import pytest
from rooms.models import Room


@pytest.fixture
def room(db):
    """Создает обычную комнату для тестов rooms"""
    return Room.objects.create(
        number='101',
        room_type='standard',
        price_per_night=3000,
        capacity=2
    )


@pytest.fixture
def luxury_room(db):
    """Создает люкс комнату для тестов rooms"""
    return Room.objects.create(
        number='999',
        room_type='lux',
        price_per_night=10000,
        capacity=4
    )


@pytest.fixture
def unavailable_room(db):
    """Создает недоступную комнату"""
    return Room.objects.create(
        number='777',
        room_type='standard',
        price_per_night=3000,
        capacity=2,
        is_available=False
    )
