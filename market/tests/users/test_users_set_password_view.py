import pytest
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST

from users.models import User


class TestUsersSetPasswordView:
    @pytest.mark.django_db
    def test_users_set_password_view(self, client, user_and_access_token, password):
        user, access_token = user_and_access_token
        data = {
            'new_password': 'new_test_password',
            'current_password': password,
        }

        response = client.post(
            '/api/users/set_password/',
            data=data,
            content_type='application/json',
            HTTP_AUTHORIZATION=access_token,
        )

        assert response.status_code == HTTP_204_NO_CONTENT, \
            f"Возвращается статус {response.status_code}, ожидался {HTTP_204_NO_CONTENT}"

        user: User = User.objects.all()[0]
        assert not user.check_password(password), 'Остался старый пароль'
        assert user.password != data['new_password'], 'Новый пароль в нехешированном виде'
        assert user.check_password(data['new_password']), 'Новый пароль не установлен'

    @pytest.mark.django_db
    def test_users_set_password_view_errors(self, client, access_token, password):
        # Обращение без токена
        data_1 = {
            'new_password': 'new_test_password',
            'current_password': password,
        }

        response_1 = client.post(
            '/api/users/set_password/',
            data=data_1,
            content_type='application/json',
        )

        assert response_1.status_code == HTTP_401_UNAUTHORIZED, \
            f"Возвращается статус {response_1.status_code}, ожидался {HTTP_401_UNAUTHORIZED}"

        # Обращение без данных
        response_2 = client.post(
            '/api/users/set_password/',
            content_type='application/json',
            HTTP_AUTHORIZATION=access_token,
        )

        assert response_2.status_code == HTTP_400_BAD_REQUEST, \
            f"Возвращается статус {response_2.status_code}, ожидался {HTTP_400_BAD_REQUEST}"

        # Обращение с пустыми данными
        data_3 = {
            'new_password': '',
            'current_password': '',
        }

        response_3 = client.post(
            '/api/users/set_password/',
            data=data_3,
            content_type='application/json',
            HTTP_AUTHORIZATION=access_token,
        )

        assert response_3.status_code == HTTP_400_BAD_REQUEST, \
            f"Возвращается статус {response_3.status_code}, ожидался {HTTP_400_BAD_REQUEST}"

        # Обращение с неверным паролем
        data_4 = {
            'new_password': 'new_test_password',
            'current_password': 'wrong_password',
        }

        response_4 = client.post(
            '/api/users/set_password/',
            data=data_4,
            content_type='application/json',
            HTTP_AUTHORIZATION=access_token,
        )

        assert response_4.status_code == HTTP_400_BAD_REQUEST, \
            f"Возвращается статус {response_4.status_code}, ожидался {HTTP_400_BAD_REQUEST}"

        assert 'current_password' in response_4.data, 'Нет ошибки о неправильном пароле'

        # Обращение с простым паролем
        data_5 = {
            'new_password': ' qwe123',
            'current_password': password,
        }

        response_5 = client.post(
            '/api/users/set_password/',
            data=data_5,
            content_type='application/json',
            HTTP_AUTHORIZATION=access_token,
        )

        assert response_5.status_code == HTTP_400_BAD_REQUEST, \
            f"Возвращается статус {response_5.status_code}, ожидался {HTTP_400_BAD_REQUEST}"
        assert 'new_password' in response_5.data, 'Нет ошибки о неправильном пароле'
