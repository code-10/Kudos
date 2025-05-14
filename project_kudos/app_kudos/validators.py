from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from .models import User, Kudo, KudoConfig
from django.utils import timezone

def validate_kudo_data(func):
    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        from_user = request.user
        to_user_id = request.data.get('to_user_id')
        message = request.data.get('message')

        if not to_user_id or not message:
            return Response({"error": "Both 'to_user_id' and 'message' are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            to_user = User.objects.get(id=to_user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        if from_user.organization != to_user.organization:
            return Response({"error": "You can only send kudos to users within your organization."}, status=status.HTTP_403_FORBIDDEN)

        current_week = timezone.now().isocalendar().week
        given_this_week = Kudo.objects.filter(from_user=from_user, created_at__week=current_week).count()
        weekly_kudos_limit = KudoConfig.objects.first().weekly_kudos_limit
        available_kudos = max(0, weekly_kudos_limit - given_this_week)

        if available_kudos <= 0:
            return Response({"error": "You have no remaining kudos for this week. Try later buddy"}, status=status.HTTP_400_BAD_REQUEST)

        request.validated_data = {'from_user': from_user, 'to_user': to_user, 'message': message}
        
        return func(self, request, *args, **kwargs)

    return wrapper
