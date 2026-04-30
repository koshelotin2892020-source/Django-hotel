# rooms/tests/test_models.py
import pytest
from rooms.models import Room


@pytest.mark.django_db
class TestRoomModel:
    """Тесты модели комнаты"""
    
    def test_can_create_room(self):
        """Можно создать комнату"""
        room = Room.objects.create(
            number='101',
            room_type='standard',
            price_per_night=3000,
            capacity=2
        )
        assert room.pk is not None
        assert room.is_available  # По умолчанию доступна
    
    def test_room_number_unique(self):
        """Номер комнаты должен быть уникальным"""
        Room.objects.create(
            number='101',
            room_type='standard',
            price_per_night=3000,
            capacity=2
        )
        
        with pytest.raises(Exception):  # IntegrityError
            Room.objects.create(
                number='101',  # Тот же номер
                room_type='lux',
                price_per_night=5000,
                capacity=4
            )
    
    def test_price_must_be_positive(self):
        """Цена должна быть положительной"""
        with pytest.raises(Exception):
            Room.objects.create(
                number='102',
                room_type='standard',
                price_per_night=-100,  # Отрицательная цена
                capacity=2
            )
    
    def test_capacity_must_be_positive(self):
        """Вместимость должна быть положительной"""
        with pytest.raises(Exception):
            Room.objects.create(
                number='103',
                room_type='standard',
                price_per_night=3000,
                capacity=0  # Невалидная вместимость
            )
    
    def test_can_change_availability(self):
        """Можно менять статус доступности комнаты"""
        room = Room.objects.create(
            number='104',
            room_type='standard',
            price_per_night=3000,
            capacity=2
        )
        
        room.is_available = False
        room.save()
        assert not room.is_available
        
        room.is_available = True
        room.save()
        assert room.is_available
    
    def test_room_type_choices(self):
        """Тип комнаты может быть только из списка"""
        # Валидные типы
        for room_type in ['standard', 'comfort', 'lux']:
            room = Room.objects.create(
                number=f'10{room_type}',
                room_type=room_type,
                price_per_night=3000,
                capacity=2
            )
            assert room.pk is not None
        
        # Невалидный тип вызовет ошибку
        with pytest.raises(Exception):
            Room.objects.create(
                number='999',
                room_type='invalid_type',
                price_per_night=3000,
                capacity=2
            )
