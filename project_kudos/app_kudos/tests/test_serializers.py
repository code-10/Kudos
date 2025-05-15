import pytest
from app_kudos.serializers import OrganizationSerializer, UserSerializer, KudoSerializer

@pytest.mark.django_db
def test_organization_serializer(organization):
    serializer = OrganizationSerializer(organization)
    assert serializer.data["name"] == "Mitratech"

@pytest.mark.django_db
def test_user_serializer(user_one):
    serializer = UserSerializer(user_one)
    assert serializer.data["username"] == "user1"

@pytest.mark.django_db
def test_kudo_serializer(kudo):
    serializer = KudoSerializer(kudo)
    assert serializer.data["message"] == "Here you go Kudos!"
