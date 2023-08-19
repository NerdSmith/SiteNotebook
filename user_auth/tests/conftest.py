import pytest
from rest_framework.reverse import reverse

from user_auth.models import User

LOGIN_URL = reverse('token_obtain_pair')


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def email():
    return "test@gmail.com"


@pytest.fixture
def password():
    return "1029qpwo"


@pytest.fixture
def user(email, password):
    return User.objects.create_user(email, password)


@pytest.fixture
def login(db, api_client, user, email, password):
    r = api_client.post(LOGIN_URL, {'email': email, 'password': password})
    body = r.json()
    if 'access' in body:
        api_client.credentials(
            HTTP_AUTHORIZATION='Bearer %s' % body['access'])
    return r.status_code, body


@pytest.fixture
def user_payload():
    return {
        "password": "1029qpwo",
        "first_name": "test",
        "last_name": "test",
        "patronymic": "test",
        "email": "testtest@gmail.com"
    }


@pytest.fixture
def user_client(api_client, user):
    api_client.force_authenticate(user)
    return api_client
