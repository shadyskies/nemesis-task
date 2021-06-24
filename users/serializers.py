from django.contrib.auth import authenticate, login
from django.contrib.auth.models import update_last_login
from rest_framework import serializers

from .models import UserModel
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('username', 'password')

    def validate(self, data):
        username = data.get("username", None)
        password = data.get("password", None)
        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password is not found.'
            )
        return user

