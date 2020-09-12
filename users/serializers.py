from rest_framework import serializers
from .models import User
from rooms import serializers as rooms_serializers


class RelatedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "avatar",
            "superhost",
        )


class TinyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "superhost")


class ReadUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = (
            "groups",
            "user_permissions",
            "password",
            "last_login",
            "is_superuser",
            "is_staff",
            "date_joined",
            "is_active",
            "favs",
        )


class WriteUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "avatar",
            "superhost",
        )

    def validate_first_name(self, value):
        return value.capitalize()


class FavsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "favs",
        )
        read_only_fileds = ("username",)
