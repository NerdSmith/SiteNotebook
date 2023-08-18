import json

import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_user_by_unauthorized(user, client, user_payload):
    url = reverse('users-list')
    response = client.post(
        url,
        user_payload,
        content_type='application/json'
    )
    assert response.status_code == status.HTTP_201_CREATED

    url = reverse('users-list')
    response = client.get(
        url
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    url = reverse(
        'users-detail',
        kwargs={'pk': 1}
    )
    response = client.get(
        url
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    url = reverse(
        'users-detail',
        kwargs={'pk': 1}
    )
    user_payload["first_name"] = "Oleg"
    response = client.put(
        url,
        data=user_payload,
        content_type='application/json'
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    url = reverse(
        'users-detail',
        kwargs={'pk': 1}
    )
    user_payload["first_name"] = "Oleg"
    response = client.patch(
        url,
        data=user_payload,
        content_type='application/json'
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    url = reverse(
        'users-detail',
        kwargs={'pk': 1}
    )
    response = client.delete(
        url
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_user_by_admin(admin_client, user_payload):
    url = reverse('users-list')
    response = admin_client.post(
        url,
        data=user_payload,
        content_type='application/json'
    )
    assert response.status_code == status.HTTP_201_CREATED

    user_id = response.data.get('id')

    url = reverse('users-list')
    response = admin_client.get(
        url
    )
    assert response.status_code == status.HTTP_200_OK

    url = reverse(
        'users-detail',
        kwargs={'pk': user_id}
    )
    response = admin_client.get(
        url
    )
    assert response.status_code == status.HTTP_200_OK

    url = reverse(
        'users-detail',
        kwargs={'pk': user_id}
    )
    user_put_payload = {"first_name": "Oleg"}
    response = admin_client.put(
        url,
        data=user_put_payload,
        content_type='application/json'
    )
    assert response.status_code == status.HTTP_200_OK

    url = reverse(
        'users-detail',
        kwargs={'pk': user_id}
    )
    user_patch_payload = {"first_name": "Oleg"}
    response = admin_client.patch(
        url,
        data=user_patch_payload,
        content_type='application/json'
    )
    assert response.status_code == status.HTTP_200_OK

    url = reverse(
        'users-detail',
        kwargs={'pk': user_id}
    )
    response = admin_client.delete(
        url
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_user_by_user(user_client, user_payload):
    url = reverse('users-list')
    response = user_client.post(
        url,
        data=json.dumps(user_payload),
        content_type='application/json'
    )
    assert response.status_code == status.HTTP_201_CREATED

    user_id = response.data.get('id')

    url = reverse('users-list')
    response = user_client.get(
        url
    )
    assert response.status_code == status.HTTP_200_OK

    url = reverse(
        'users-detail',
        kwargs={'pk': user_id}
    )
    response = user_client.get(
        url
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN

    url = reverse(
        'users-detail',
        kwargs={'pk': user_id}
    )
    user_put_payload = {"first_name": "Oleg"}
    response = user_client.put(
        url,
        data=user_put_payload,
        content_type='application/json'
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN

    url = reverse(
        'users-detail',
        kwargs={'pk': user_id}
    )
    user_patch_payload = {"first_name": "Oleg"}
    response = user_client.patch(
        url,
        data=user_patch_payload,
        content_type='application/json'
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN

    url = reverse(
        'users-detail',
        kwargs={'pk': user_id}
    )
    response = user_client.delete(
        url
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
