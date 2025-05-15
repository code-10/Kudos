import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status

client = APIClient()

@pytest.mark.django_db
def test_fetch_same_org_users(user_one, user_two):
    client.force_authenticate(user=user_one)
    response = client.get(reverse("user-same-organization-users"))
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["username"] == "user2"

@pytest.mark.django_db
def test_available_kudos(user_one, kudo_config):
    client.force_authenticate(user=user_one)
    response = client.get(reverse("kudo-available-kudos"))
    assert response.status_code == status.HTTP_200_OK
    assert response.data["available_kudos"] == 3
