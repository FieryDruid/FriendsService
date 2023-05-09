from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as i18n
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from friendsservice.api_v1.user.handlers import ValidatePasswordHandler
from friendsservice.api_v1.user.serializers import (
    UserDataSerializer, UserCreationErrorSerializer, UsernameSerializer, CreateFriendshipErrorSerializer,
    SentFriendshipRequestsSerializer, ReceivedFriendshipRequestsSerializer, UserFriendsListSerializer
)
from friendsservice.friendship.exceptions import (
    UserCannotBeFriendError, FriendshipRequestAlreadyExistsError, UserDoesNotExistsError,
    FriendshipRequestDoesNotExistsError, HasActiveFriendship, UserNotInFriendsListError
)
from friendsservice.friendship.models import FriendshipStatus
from friendsservice.friendship.services.add_to_friends import AddToFriendsService
from friendsservice.friendship.services.change_status import ChangeFriendshipStatusService
from friendsservice.friendship.services.check_status import CheckFriendshipStatusService
from friendsservice.friendship.services.delete_from_friends import DeleteFromFriendsService
from friendsservice.friendship.services.get_friends_list import GetFriendsListService
from friendsservice.friendship.services.received_requests import GetReceivedFriendshipRequestsService
from friendsservice.friendship.services.sent_requests import GetSentFriendshipRequestsService

User = get_user_model()


class CreateUserView(APIView):

    @extend_schema(
        description=i18n('Create new user'),
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

        User.objects.create(
            username=serializer_data['username'],
            password=make_password(serializer_data['password'])
        )
        return Response(status=200)


class AddUserView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        description=i18n('Send friendship request to user'),
        request=UsernameSerializer,
        responses={
            200: None,
            400: CreateFriendshipErrorSerializer,
        },
        methods=['POST']
    )
    def post(self, request: Request) -> Response:
        serializer = UsernameSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer_data = serializer.data

        try:
            AddToFriendsService(sender=request.user, recipient_username=serializer_data['username'])()
        except (UserCannotBeFriendError, UserDoesNotExistsError):
            return Response(data={'error': 'User cannot be friend'}, status=400)
        except FriendshipRequestAlreadyExistsError:
            return Response(data={'error': 'Friendship request already sent'}, status=400)
        return Response(status=200)


class UserSentFriendshipView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        description=i18n('Get sent friendship requests list'),
        responses={
            200: SentFriendshipRequestsSerializer(many=True)
        },
        methods=['GET']
    )
    def get(self, request: Request) -> Response:
        service_result = GetSentFriendshipRequestsService(user=request.user)()
        serialized_data = SentFriendshipRequestsSerializer(data=service_result, many=True)
        serialized_data.is_valid()
        return Response(data=serialized_data.data, status=200)


class UserReceivedFriendshipView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        description=i18n('Get received friendship requests list'),
        responses={
            200: ReceivedFriendshipRequestsSerializer(many=True)
        },
        methods=['GET']
    )
    def get(self, request: Request) -> Response:
        service_result = GetReceivedFriendshipRequestsService(user=request.user)()
        serialized_data = ReceivedFriendshipRequestsSerializer(data=service_result, many=True)
        serialized_data.is_valid()
        return Response(data=serialized_data.data, status=200)


class AcceptFriendshipRequestView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        description=i18n('Accept friendship request'),
        responses={
            200: None
        },
        methods=['GET']
    )
    def get(self, request: Request, **kwargs) -> Response:
        try:
            ChangeFriendshipStatusService(friendship=kwargs['friendship_id'], status=FriendshipStatus.CONFIRMED)()
        except FriendshipRequestDoesNotExistsError:
            return Response({'error': 'Friendship request not found'}, status=404)
        return Response(status=200)


class DeclineFriendshipRequestView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        description=i18n('Decline friendship request'),
        responses={
            200: None
        },
        methods=['GET']
    )
    def get(self, request: Request, **kwargs) -> Response:
        friendship_id = kwargs['friendship_id']
        try:
            ChangeFriendshipStatusService(friendship=kwargs['friendship_id'], status=FriendshipStatus.DECLINED)()
        except FriendshipRequestDoesNotExistsError:
            return Response({'error': f'Not found active friendship request with id {friendship_id}'}, status=404)
        return Response(status=200)


class UserFriendshipView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        description=i18n('Get friendship with user status'),
        responses={
            200: None
        },
        methods=['GET']
    )
    def get(self, request: Request, **kwargs) -> Response:
        target_username = kwargs['username']
        try:
            CheckFriendshipStatusService(target_username=target_username)()
        except FriendshipRequestDoesNotExistsError:
            return Response({'message': f'Not found active friendship with {target_username}'}, status=200)
        except HasActiveFriendship as exc:
            return Response({'message': exc.friendship_status}, status=200)
        return Response(status=400)

    @extend_schema(
        description=i18n('Delete user from friends'),
        responses={
            200: None,
            404: None
        },
        methods=['DELETE']
    )
    def delete(self, request: Request, **kwargs) -> Response:
        try:
            DeleteFromFriendsService(sender=request.user, target_username=kwargs['username'])()
        except (UserNotInFriendsListError, UserDoesNotExistsError):
            return Response(status=404)
        return Response(status=200)


class UserFriendsView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        description=i18n('Get friends list'),
        responses={
            200: UserFriendsListSerializer()
        },
        methods=['GET']
    )
    def get(self, request: Request) -> Response:
        return Response(GetFriendsListService(user=request.user)(), status=200)
