import pytest
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED

from users.serializers import CurrentUserSerializer


class TestUserProfileView:
    @pytest.mark.django_db
    def test_user_profile_view(self, client, user_and_access_token):
        user, access_token = user_and_access_token

        response = client.get(
            '/api/users/me/',
            HTTP_AUTHORIZATION=access_token,
        )
        assert response.status_code == HTTP_200_OK, \
            f"Возвращается статус {response.status_code}, ожидался {HTTP_200_OK}"

        user_json = CurrentUserSerializer(user).data
        assert response.data == user_json, 'Данные пользователя не совпадают'

    @pytest.mark.django_db
    def test_user_profile_view_errors(self, client, access_token):
        # Обращение без токена
        response_1 = client.get(
            '/api/users/me/',
        )
        assert response_1.status_code == HTTP_401_UNAUTHORIZED, \
            f"Возвращается статус {response_1.status_code}, ожидался {HTTP_401_UNAUTHORIZED}"

        # Обращение неверным токеном
        response_2 = client.get(
            '/api/users/me/',
            HTTP_AUTHORIZATION=access_token + '1',
        )
        assert response_2.status_code == HTTP_401_UNAUTHORIZED, \
            f"Возвращается статус {response_2.status_code}, ожидался {HTTP_401_UNAUTHORIZED}"
