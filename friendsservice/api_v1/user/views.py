from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from drf_spectacular.utils import extend_schema
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from friendsservice.api_v1.user.handlers import ValidatePasswordHandler
from friendsservice.api_v1.user.serializers import UserDataSerializer, UserCreationErrorSerializer

User = get_user_model()


class UserView(APIView):

    @extend_schema(
        description='Create new user',
        request=UserDataSerializer,
        responses={
            200: None,
            400: UserCreationErrorSerializer,
        },
        methods=['POST']
    )
    def post(self, request: Request) -> Response:
        serializer = UserDataSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer_data = serializer.data

        try:
            ValidatePasswordHandler(serializer_data['password']).validate()
        except ValidationError as exc:
            return Response({'error': {'password': exc.messages}}, status=400)

        already_exists = User.objects.filter(username=serializer_data['username']).exists()
        if already_exists:
            return Response({'error': {'username': ['User already exists']}}, status=400)

        User(username=serializer_data['username'], password=make_password(serializer_data['password'])).save()
        return Response(status=200)
