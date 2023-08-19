import json

import pytest
from rest_framework import status
from rest_framework.reverse import reverse


@pytest.mark.django_db
def test_bookmark_create(user_client, bookmark_payload, valid_bookmark_answer):
    url = reverse('bookmarks-list')
    response = user_client.post(
        url,
        data=json.dumps(bookmark_payload),
        content_type='application/json'
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["title"] == valid_bookmark_answer["title"]
    assert response.data["description"] == valid_bookmark_answer["description"]
    assert response.data["link"] == valid_bookmark_answer["link"]
    assert response.data["link_type"] == valid_bookmark_answer["link_type"]
    assert response.data["image"] == valid_bookmark_answer["image"]


@pytest.mark.django_db
def test_bookmark_delete(user_client, bookmark):
    url = reverse(
        'bookmarks-detail',
        kwargs={'pk': bookmark.pk}
    )
    response = user_client.delete(
        url
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
