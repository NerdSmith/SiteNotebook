from functools import partial

import pytest
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

REFRESH_TOKEN_URL = reverse('token_refresh')
LOGOUT_URL = reverse('token_blacklist')


@pytest.mark.django_db
def test_logout_response_200(user, api_client, login):
    _, body = login
    print("asd", body)
    data = {'refresh': body['refresh']}
    r = api_client.post(LOGOUT_URL, data)
    body = r.content
    assert r.status_code == status.HTTP_200_OK
    assert body == body


@pytest.mark.django_db
def test_logout_with_bad_refresh_token_response_400(user, api_client, login):
    _, body = login
    data = {'refresh': 'dsf.sdfsdf.sdf'}
    r = api_client.post(LOGOUT_URL, data)
    body = r.json()
    assert r.status_code == status.HTTP_401_UNAUTHORIZED
    assert body == body


@pytest.mark.django_db
def test_logout_refresh_token_in_blacklist(user, api_client, login):
    _, body = login
    r = api_client.post(LOGOUT_URL, body)
    with pytest.raises(TokenError):
        RefreshToken(body['refresh'])

