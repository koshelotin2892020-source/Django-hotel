# users/tests/test_models.py
import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from users.models import AccountInfo

CustomUser = get_user_model()


@pytest.mark.django_db
class TestCustomUserModel:
    """Тесты модели пользователя"""
    
    def test_can_create_user(self):
        """Можно создать пользователя"""
        user = CustomUser.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        assert user.pk is not None
        assert user.check_password('testpass123')
    
    def test_username_required(self):
        """Username обязателен"""
        with pytest.raises(Exception):
            CustomUser.objects.create_user(username='', password='pass')


@pytest.mark.django_db
class TestAccountInfoModel:
    """Тесты профиля пользователя"""
    
    def test_can_create_account_info(self, user):
        """Можно создать профиль"""
        account_info = AccountInfo.objects.create(
            account=user,
            first_name='Иван',
            last_name='Петров',
            phone='+7 123 456-78-90',
            email='ivan@gmail.com'
        )
        assert account_info.pk is not None
    
    def test_account_info_required_fields(self, user):
        """Обязательные поля first_name, last_name, phone, email"""
        with pytest.raises(ValidationError):
            account = AccountInfo(account=user)
            account.full_clean()  # Вызовет ошибку валидации
    
    def test_phone_unique(self, user):
        """Номер телефона должен быть уникальным"""
        AccountInfo.objects.create(
            account=user,
            first_name='Иван',
            last_name='Петров',
            phone='+7 123 456-78-90',
            email='ivan@gmail.com'
        )
        
        user2 = CustomUser.objects.create_user(username='testuser2', password='pass')
        with pytest.raises(IntegrityError):
            AccountInfo.objects.create(
                account=user2,
                first_name='Петр',
                last_name='Сидоров',
                phone='+7 123 456-78-90',  # Тот же телефон
                email='petr@gmail.com'
            )
    
    def test_email_unique(self, user):
        """Email должен быть уникальным"""
        AccountInfo.objects.create(
            account=user,
            first_name='Иван',
            last_name='Петров',
            phone='+7 123 456-78-90',
            email='ivan@gmail.com'
        )
        
        user2 = CustomUser.objects.create_user(username='testuser2', password='pass')
        with pytest.raises(IntegrityError):
            AccountInfo.objects.create(
                account=user2,
                first_name='Петр',
                last_name='Сидоров',
                phone='+7 999 888-77-66',
                email='ivan@gmail.com'  # Тот же email
            )
    
    def test_phone_validation(self, user):
        """Валидатор номера телефона работает"""
        # Валидный номер
        account_valid = AccountInfo(
            account=user,
            first_name='Иван',
            last_name='Петров',
            phone='+7 123 456-78-90',
            email='ivan@gmail.com'
        )
        account_valid.full_clean()  # Не должно быть ошибки
        
        # Невалидный номер
        account_invalid = AccountInfo(
            account=user,
            first_name='Иван',
            last_name='Петров',
            phone='123',  # Слишком короткий
            email='ivan@gmail.com'
        )
        with pytest.raises(ValidationError):
            account_invalid.full_clean()
    
    def test_email_validation(self, user):
        """Валидатор email работает - только gmail или mail.ru"""
        # Валидные email
        for email in ['user@gmail.com', 'user@mail.ru']:
            account = AccountInfo(
                account=user,
                first_name='Иван',
                last_name='Петров',
                phone='+7 123 456-78-90',
                email=email
            )
            account.full_clean()  # Не должно быть ошибки
        
        # Невалидный email (другой домен)
        account_invalid = AccountInfo(
            account=user,
            first_name='Иван',
            last_name='Петров',
            phone='+7 123 456-78-90',
            email='user@yandex.ru'
        )
        with pytest.raises(ValidationError):
            account_invalid.full_clean()
    
    def test_one_to_one_relation(self, user):
        """Связь один к одному с пользователем"""
        account_info = AccountInfo.objects.create(
            account=user,
            first_name='Иван',
            last_name='Петров',
            phone='+7 123 456-78-90',
            email='ivan@gmail.com'
        )
        
        # Проверяем related_name='info'
        assert user.info == account_info
    
    def test_delete_user_deletes_profile(self, user):
        """При удалении пользователя удаляется и его профиль"""
        account_info = AccountInfo.objects.create(
            account=user,
            first_name='Иван',
            last_name='Петров',
            phone='+7 123 456-78-90',
            email='ivan@gmail.com'
        )
        
        user.delete()
        
        with pytest.raises(AccountInfo.DoesNotExist):
            account_info.refresh_from_db()
