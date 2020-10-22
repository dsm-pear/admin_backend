from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import AdminTbl
from .services import HashService

User = get_user_model()

class UserCreateSerializer(serializers.Serializer):
    email = serializers.CharField(required=True, max_length=45)
    password = serializers.CharField(required=True, max_length=64)

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            password=HashService.hash_string_to_password(validated_data['password'])
        )

        # user.save()
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True, max_length=45)
    password = serializers.CharField(required=True, max_length=64)
