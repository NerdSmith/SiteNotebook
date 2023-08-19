import json

import pytest
from rest_framework import status
from rest_framework.reverse import reverse


@pytest.mark.django_db
def test_collection_create(user_client, collection_payload):
    url = reverse('collections-list')
    response = user_client.post(
        url,
        data=json.dumps(collection_payload),
        content_type='application/json'
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["title"] == collection_payload["title"]
    assert response.data["description"] == collection_payload["description"]


@pytest.mark.django_db
def test_collection_delete(user_client, collection):
    url = reverse(
        'collections-detail',
        kwargs={'pk': collection.pk}
    )
    response = user_client.delete(
        url
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_collection_update(user_client, collection, collection_payload):
    url = reverse(
        'collections-detail',
        kwargs={'pk': collection.pk}
    )
    collection_payload["title"] = "nottest"
    collection_payload["description"] = "nottesttest"
    response = user_client.patch(
        url,
        data=json.dumps(collection_payload),
        content_type='application/json'
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data['title'] == 'nottest'
    assert response.data['description'] == 'nottesttest'


@pytest.mark.django_db
def test_bookmark_collection_add_rm(user_client, collection, bookmark):
    url = reverse(
        'collections-add-bookmarks',
        kwargs={'pk': collection.pk}
    )
    response = user_client.patch(
        url,
        data=json.dumps({"bookmarks": [bookmark.pk]}),
        content_type='application/json'
    )
    assert response.status_code == status.HTTP_200_OK

    url = reverse(
        'collections-remove-bookmarks',
        kwargs={'pk': collection.pk}
    )
    response = user_client.patch(
        url,
        data=json.dumps({"bookmarks": [bookmark.pk]}),
        content_type='application/json'
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
