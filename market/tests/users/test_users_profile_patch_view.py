import pytest
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED

from users.models import User


class TestUsersProfilePatchView:
    @pytest.mark.django_db
    def test_users_profile_patch_view(self, client, user_and_access_token):
        user, access_token = user_and_access_token
        data = {
            "first_name": 'test_first_name',
            "last_name": 'test_last_name',
            "phone": '+79999999999',
            "email": 'test_email@mail.ru',
        }

        response = client.patch(
            '/api/users/me/',
            data=data,
            content_type='application/json',
            HTTP_AUTHORIZATION=access_token,

        )

        assert response.status_code == HTTP_200_OK, \
            f"Возвращается статус {response.status_code}, ожидался {HTTP_200_OK}"

        user = User.objects.all()[0]

        assert user.first_name == data['first_name'], 'first_name пользователя не совпадает с переданным значением'
        assert user.last_name == data['last_name'], 'last_name пользователя не совпадает с переданным значением'
        assert user.phone == data['phone'], 'phone пользователя не совпадает с переданным значением'
        assert user.email == data['email'], 'email пользователя не совпадает с переданным значением'

    @pytest.mark.django_db
    def test_users_profile_patch_view_errors(self, client, access_token):
        # Обращение с пустыми данными
        data_2 = {
            "first_name": '',
            "last_name": '',
            "phone": '',
            "email": '',
            "password": '',
        }

        response_2 = client.patch(
            '/api/users/me/',
            data=data_2,
            content_type='application/json',
            HTTP_AUTHORIZATION=access_token
        )

        assert response_2.status_code == HTTP_400_BAD_REQUEST, \
            f"Возвращается статус {response_2.status_code}, ожидался {HTTP_400_BAD_REQUEST}"

        # Обращение с без токена
        data_3 = {
            "first_name": '',
            "last_name": '',
            "phone": '',
            "email": '',
            "password": '',
        }

        response_3 = client.patch(
            '/api/users/me/',
            data=data_3,
            content_type='application/json',
        )

        assert response_3.status_code == HTTP_401_UNAUTHORIZED, \
            f"Возвращается статус {response_3.status_code}, ожидался {HTTP_401_UNAUTHORIZED}"
        