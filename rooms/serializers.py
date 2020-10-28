from rest_framework import serializers
from .models import Room, Photo
from users.serializers import TinyUserSerializer, RelatedUserSerializer, UserSerializer


"""class RoomSerializer(serializers.Serializer):
    name = serializers.CharField(max_lengt1h=200)
    price = serializers.IntegerField(default=1)
    bedrooms = serializers.IntegerField(default=1)
    bathrooms = serializers.IntegerField(default=1)"""


class SmallPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('file', 'caption', 'room', )


class ReadRoomSerializer(serializers.ModelSerializer):
    user = TinyUserSerializer()

    class Meta:
        model = Room
        exclude = ("modified",)


class WriteRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        exclude = ("user", "modified", "created")

    def validate(self, data):
        if self.instance is None:
            beds = data["beds"]
            if beds < 3:
                raise serializers.ValidationError("Your room is too small.")
        print(data)
        return data


class RoomSerializer(serializers.ModelSerializer):
    in_favorite = serializers.SerializerMethodField()

    def get_in_favorite(self, obj):
        request = self.context.get("request")
        if request is not None:
            user = request.user
            if user is not None and user.is_authenticated:
                return obj in user.favs.all()
            else:
                return None
        else:
            return None

    user = UserSerializer(read_only=True)
    photos = SmallPhotoSerializer(many=True)

    def create(self, validated_data):
        request = self.context.get("request")
        if request.user is not None and request.user.is_authenticated:
            room = Room.objects.create(**validated_data, user=request.user)
            return room
        else:
            return None

    class Meta:
        model = Room
        exclude = ("modified",)
        read_only_fields = ("user", "id", "created", "modified")

    # class WriteRoomSerializer(serializers.Serializer):
    """ 
    name = serializers.CharField(max_length=140)
    address = serializers.CharField(max_length=140)
    price = serializers.IntegerField(help_text="USD per night")
    beds = serializers.IntegerField(default=1)
    lat = serializers.DecimalField(max_digits=10, decimal_places=6)
    lng = serializers.DecimalField(max_digits=10, decimal_places=6)
    bedrooms = serializers.IntegerField(default=1)
    bathrooms = serializers.IntegerField(default=1)
    check_in = serializers.TimeField(default="00:00:00")
    check_out = serializers.TimeField(default="00:00:00")
    instant_book = serializers.BooleanField(default=False)

    def create(self, validated_data):
        return Room.objects.create(**validated_data)

    def validate(self, data):
        if self.instance is None:
            beds = data["beds"]
            if beds < 3:
                raise serializers.ValidationError("Your room is too small.")
        print(data)
        return data

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.address = validated_data.get("address", instance.address)
        instance.price = validated_data.get("price", instance.price)
        instance.beds = validated_data.get("beds", instance.beds)
        instance.lat = validated_data.get("lat", instance.lat)
        instance.lng = validated_data.get("lng", instance.lng)
        instance.bedrooms = validated_data.get("bedrooms", instance.bedrooms)
        instance.bathrooms = validated_data.get("bathrooms", instance.bathrooms)
        instance.check_in = validated_data.get("check_in", instance.check_in)
        instance.check_out = validated_data.get("check_out", instance.check_out)
        instance.instant_book = validated_data.get(
            "instant_book", instance.instant_book
        )
        instance.save()
        return instance
    """


class TinyRoomSerializer(serializers.ModelSerializer):
    user = RelatedUserSerializer()

    class Meta:
        model = Room
        fields = ("name", "user", "price", "bedrooms", "bathrooms", "beds")


class RelatedRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ("name", "price", "bedrooms", "bathrooms", "beds")