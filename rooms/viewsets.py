from rest_framework import viewsets
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Room
from .serializers import RoomSerializer, TinyRoomSerializer
from .permissions import IsRoomOwner


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            permission_classes = [
                AllowAny,
            ]
        elif self.action == "create":
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [
                IsRoomOwner,
            ]
        return [permission() for permission in permission_classes]
