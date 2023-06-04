import pytest
from factory import Faker
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from users.models import User


class TestUsersCreateView:
    @pytest.mark.django_db
    def test_users_create_view(self, client):
        data = {
            "first_name": 'test_first_name',
            "last_name": 'test_last_name',
            "phone": '+79999999999',
            "email": 'test_email@mail.ru',
            "password": 'test_password',
        }

        response = client.post(
            '/api/users/',
            data=data,
            content_type='application/json',
        )

        assert response.status_code == HTTP_201_CREATED, \
            f"Возвращается статус {response.status_code}, ожидался {HTTP_201_CREATED}"

        user = User.objects.all()[0]

        assert user.first_name == data['first_name'], 'first_name пользователя не совпадает с переданным значением'
        assert user.last_name == data['last_name'], 'last_name пользователя не совпадает с переданным значением'
        assert user.phone == data['phone'], 'phone пользователя не совпадает с переданным значением'
        assert user.email == data['email'], 'email пользователя не совпадает с переданным значением'
        assert user.password != data['password'], 'password пользователя не в хешированном виде'
        assert user.check_password(data['password']), 'Пароли не совпадают'

    @pytest.mark.django_db
    def test_users_create_view_errors(self, client):
        # Обращение без данных
        response_1 = client.post(
            '/api/users/',
        )

        assert response_1.status_code == HTTP_400_BAD_REQUEST, \
            f"Возвращается статус {response_1.status_code}, ожидался {HTTP_400_BAD_REQUEST}"

        # Обращение с пустыми данными
        data_2 = {
            "first_name": '',
            "last_name": '',
            "phone": '',
            "email": '',
            "password": '',
        }

        response_2 = client.post(
            '/api/users/',
            data=data_2,
            content_type='application/json',
        )

        assert response_2.status_code == HTTP_400_BAD_REQUEST, \
            f"Возвращается статус {response_2.status_code}, ожидался {HTTP_400_BAD_REQUEST}"
