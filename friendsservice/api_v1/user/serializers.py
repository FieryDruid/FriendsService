from rest_framework import serializers


class UserDataSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class UserErrorSerializer(serializers.Serializer):
    password = serializers.ListField(child=serializers.CharField(), required=False)
    username = serializers.ListField(child=serializers.CharField(), required=False)


class UserCreationErrorSerializer(serializers.Serializer):
    error = UserErrorSerializer()
