from django.contrib.auth.models import User
from rest_framework import serializers

from friendsservice.friendship.models import UserFriendship


class UserDataSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class UserErrorSerializer(serializers.Serializer):
    password = serializers.ListField(child=serializers.CharField(), required=False)
    username = serializers.ListField(child=serializers.CharField(), required=False)


class UserCreationErrorSerializer(serializers.Serializer):
    error = UserErrorSerializer()


class CreateFriendshipErrorSerializer(serializers.Serializer):
    error = serializers.CharField()


class UsernameSerializer(serializers.Serializer):
    username = serializers.CharField()


class UsernameField(serializers.RelatedField):
    username = serializers.CharField()

    def to_representation(self, value: User) -> str:
        return value.username


class SentFriendshipRequestsSerializer(serializers.ModelSerializer):
    recipient = UsernameField(read_only=True)

    class Meta:
        model = UserFriendship
        fields = ('id', 'recipient')


class ReceivedFriendshipRequestsSerializer(serializers.ModelSerializer):
    sender = UsernameField(read_only=True)

    class Meta:
        model = UserFriendship
        fields = ('id', 'sender')


class UserFriendsListSerializer(serializers.Serializer):
    friends = serializers.ListField(child=serializers.CharField(), allow_empty=True)
