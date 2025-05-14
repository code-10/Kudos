import pytest
from django.contrib.auth import get_user_model
from app_kudos.models import Organization, Kudo, KudoConfig

User = get_user_model()

@pytest.mark.django_db
def test_organization_creation(organization, organization_two):
    assert organization.name == "Mitratech"
    assert organization_two.name == "Eurofins"
    assert Organization.objects.count() == 2

@pytest.mark.django_db
def test_user_creation(user_one, organization):
    assert user_one.username == "user1"
    assert user_one.organization == organization

@pytest.mark.django_db
def test_superuser_creation(organization):
    superuser = User.objects.create_superuser(username="admin", password="admin", organization=organization)
    assert superuser.is_superuser
    assert superuser.organization == organization

@pytest.mark.django_db
def test_kudo_creation(kudo, user_one, user_two):
    assert kudo.from_user == user_one
    assert kudo.to_user == user_two
    assert kudo.message == "Here you go Kudos!"
    assert Kudo.objects.count() == 1

@pytest.mark.django_db
def test_kudo_config_creation(kudo_config):
    assert kudo_config.weekly_kudos_limit == 3