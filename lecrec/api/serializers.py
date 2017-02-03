from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from api.models import Record
from django.contrib.auth.models import User
import time

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class UserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'token', )

    def get_token(self, obj):
        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token


class RecordSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Record
        fields = (
            'id', 'user', 'title', 'text',
            'filename', 'file', 'duration', 'created',
        )