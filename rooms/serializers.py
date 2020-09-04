from rest_framework import serializers
from .models import Room
from users.serializers import TinyUserSerializer


"""class RoomSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    price = serializers.IntegerField(default=1)
    bedrooms = serializers.IntegerField(default=1)
    bathrooms = serializers.IntegerField(default=1)"""


class RoomSerializer(serializers.ModelSerializer):
    user = TinyUserSerializer()

    class Meta:
        model = Room
        fields = '__all__'
