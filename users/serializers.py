from rest_framework import serializers
from .models import User
from rooms import serializers as rooms_serializers


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "avatar",
            "superhost",
            "password",
        )
        read_only_fields = (
            "id",
            "avatar",
            "superhost",
        )

    def create(self, validated_data):
        password = validated_data.get("password")
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user


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
