import pytest
from django.contrib.auth import get_user_model
from app_kudos.models import Organization, Kudo, KudoConfig

User = get_user_model()

@pytest.fixture
def organization():
    return Organization.objects.create(name="Mitratech")

@pytest.fixture
def organization_two():
    return Organization.objects.create(name="Eurofins")

@pytest.fixture
def kudo_config():
    return KudoConfig.objects.create(weekly_kudos_limit=3)

@pytest.fixture
def user_one(organization):
    return User.objects.create_user(username="user1", password="password1", organization=organization)

@pytest.fixture
def user_two(organization):
    return User.objects.create_user(username="user2", password="password2", organization=organization)

@pytest.fixture
def user_three(organization_two):
    return User.objects.create_user(username="user3", password="password3", organization=organization_two)

@pytest.fixture
def kudo(user_one, user_two):
    return Kudo.objects.create(from_user=user_one, to_user=user_two, message="Here you go Kudos!")
