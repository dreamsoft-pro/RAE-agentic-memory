from rest_framework.test import APIClient
from rest_framework import status
import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_health_check():
    client = APIClient()
    url = reverse('health_check')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['status'] == 'ok'
    assert response.data['service'] == 'screenwatcher-core'
