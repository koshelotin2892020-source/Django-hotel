# booking/tests/test_models.py
import pytest
from datetime import date, timedelta
from booking.models import Booking


@pytest.mark.django_db
class TestBookingModel:
    """Тесты модели бронирования"""
    
    def test_can_create_booking(self, user, room):
        """Можно создать бронь"""
        booking = Booking.objects.create(
            client=user,
            room=room,
            booking_date=date.today(),
            expiration_date=date.today() + timedelta(days=2)
        )
        assert booking.pk is not None
        assert booking.status == 'sleeping'  # Статус по умолчанию
    
    def test_booking_dates_required(self, user, room):
        """Даты обязательны для заполнения"""
        with pytest.raises(Exception):  # IntegrityError
            Booking.objects.create(
                client=user,
                room=room,
                booking_date=None,
                expiration_date=None
            )
    
    def test_can_change_status(self, user, room):
        """Можно менять статус брони"""
        booking = Booking.objects.create(
            client=user,
            room=room,
            booking_date=date.today(),
            expiration_date=date.today() + timedelta(days=2)
        )
        
        booking.status = 'active'
        booking.save()
        assert booking.status == 'active'
        
        booking.status = 'dead'
        booking.save()
        assert booking.status == 'dead'
    
    def test_booking_without_client(self, room):
        """Бронь может быть без клиента (null=True)"""
        booking = Booking.objects.create(
            client=None,
            room=room,
            booking_date=date.today(),
            expiration_date=date.today() + timedelta(days=2)
        )
        assert booking.client is None
        assert booking.pk is not None
    
    def test_delete_room_deletes_booking(self, user, room):
        """При удалении комнаты удаляются все ее брони"""
        booking = Booking.objects.create(
            client=user,
            room=room,
            booking_date=date.today(),
            expiration_date=date.today() + timedelta(days=2)
        )
        room.delete()
        
        with pytest.raises(Booking.DoesNotExist):
            booking.refresh_from_db()
    
    def test_delete_user_keeps_booking(self, user, room):
        """При удалении пользователя бронь остается (client становится null)"""
        booking = Booking.objects.create(
            client=user,
            room=room,
            booking_date=date.today(),
            expiration_date=date.today() + timedelta(days=2)
        )
        user.delete()
        
        booking.refresh_from_db()
        assert booking.client is None  # Стало null
        assert booking.room == room     # Комната осталась
