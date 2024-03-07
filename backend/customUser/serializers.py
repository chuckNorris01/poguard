from datetime import timedelta, datetime
import pytz

from django.contrib.auth import authenticate

from djoser.serializers import UserCreateSerializer

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'email',
            'name'
        )


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = CustomUser
        fields = ('id', 'email', 'img', 'name', 'password', 'role')

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128, write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    role = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    expires_at = serializers.DateTimeField(read_only=True)
    expires_in = serializers.IntegerField(read_only=True)


    def validate(self, data):
        email = data['email']
        password = data['password']
        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid login credentials")

        try:
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh)
            access_token = str(refresh.access_token)

            expiration_time_seconds = refresh.access_token.lifetime.total_seconds()
            
            expires_in = int(expiration_time_seconds)
            
            norway_timezone = pytz.timezone('Europe/Oslo')
            expires_at = datetime.now(norway_timezone) + timedelta(seconds=expiration_time_seconds)

            validation = {
                'access': access_token,
                'refresh': refresh_token,
                'email': user.email,
                'name': user.name,
                'role': user.role,
                'expires_at': expires_at,
                'expires_in': expires_in,
            }
            return validation
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Invalid login credentials")