from app_kudos.validators import validate_kudo_data, validate_login_data, validate_register_data
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .custom_exceptions import InvalidCredentialsError, MissingFieldsError, OrganizationNotFoundError
from .models import Kudo, KudoConfig, Organization, User
from .serializers import KudoSerializer, UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.db.models import Subquery, OuterRef

'''
    Contains all the logic related to kudo model since we are using ModelViewSet of DRF
'''
class KudoViewSet(viewsets.ModelViewSet):
    queryset = Kudo.objects.all()
    serializer_class = KudoSerializer
    permission_classes = [IsAuthenticated]

    '''
        Provides all the kudos received from other users
    '''
    @action(detail=False, methods=["get"], url_path="received")
    def received_kudos(self, request):
        user = request.user
        received_kudos = Kudo.objects.filter(to_user=user)
        serializer = self.get_serializer(received_kudos, many=True)
        return Response(serializer.data)

    '''
        Provides all the kudos given to other users
    '''
    @action(detail=False, methods=["get"], url_path="given")
    def given_kudos(self, request):
        user = request.user
        given_kudos = Kudo.objects.filter(from_user=user)
        serializer = self.get_serializer(given_kudos, many=True)
        return Response(serializer.data)

    '''
        Fetch all the available kudos for a user (as of now configured as 3 but can be changed in admin)
    '''
    @action(detail=False, methods=["get"], url_path="available-kudos")
    def available_kudos(self, request):
        user = request.user
        current_week = timezone.now().isocalendar().week
        given_this_week = Kudo.objects.filter(from_user=user, created_at__week=current_week).count()
        weekly_kudos_limit = KudoConfig.objects.first().weekly_kudos_limit
        available_kudos = max(0, weekly_kudos_limit - given_this_week)
        return Response({"available_kudos": available_kudos})

    '''
        Main logic of giving (upto weekly limit of) kudos to people
    '''
    @action(detail=False, methods=["post"], url_path="give")
    @validate_kudo_data
    def give_kudo(self, request):
        validated_data = request.validated_data
        from_user = validated_data['from_user']
        to_user = validated_data['to_user']
        message = validated_data['message']
        kudo = Kudo.objects.create(from_user=from_user, to_user=to_user, message=message)
        return Response(KudoSerializer(kudo).data, status=status.HTTP_201_CREATED)


'''
    Contains all the logic related to user model since we are using ModelViewSet of DRF
'''
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    '''
        Gets the current user who is logged in
    '''
    @action(detail=False, methods=["get"], url_path="current_user", permission_classes=[IsAuthenticated])
    def current_user(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    '''
        Registers a new user
    '''
    @action(detail=False, methods=["post"], url_path="register")
    @validate_register_data
    def register_user(self, request):
        username = request.data["username"]
        password = request.data["password"]
        email = request.data["email"]
        organization_id = request.data["organization_id"]

        try:
            organization = Organization.objects.get(id=organization_id)
        except Organization.DoesNotExist:
            raise OrganizationNotFoundError("Organization not found.")

        user = User.objects.create_user(username=username, password=password, email=email, organization=organization)
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    '''
        Login a user and provide access token which will be used for all other endpoints
    '''
    @action(detail=False, methods=["post"], url_path="login")
    @validate_login_data
    def login_user(self, request):
        username = request.data["username"]
        password = request.data["password"]

        user = authenticate(request, username=username, password=password)
        
        if user is None:
            raise InvalidCredentialsError("Invalid credentials.")

        refresh = RefreshToken.for_user(user)
        return Response({
            "access_token": str(refresh.access_token)
        }, status=status.HTTP_200_OK)

    '''
        Fetch all users who belong to same organization to give kudos to
    '''
    @action(detail=False, methods=["get"], url_path="same-organization-users", permission_classes=[IsAuthenticated])
    def same_organization_users(self, request):
        user = request.user
        organization = user.organization
        given_kudos_user_ids = Kudo.objects.filter(from_user=user).values_list('to_user_id', flat=True)
        same_org_users = User.objects.filter(organization=organization).exclude(id=user.id).exclude(id__in=given_kudos_user_ids)
        serializer = self.get_serializer(same_org_users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    '''
        Get all organizations registered which is required during registration of a user
    '''
    @action(detail=False, methods=["get"], url_path="organizations")
    def organizations(self, request):
        organizations = Organization.objects.all().values("id", "name")
        return Response(list(organizations), status=status.HTTP_200_OK)