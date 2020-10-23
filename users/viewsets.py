from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework import viewsets
from rest_framework.decorators import permission_classes, action
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.status import HTTP_401_UNAUTHORIZED

from rest_condition import Or

import jwt

from .models import User
from .serializers import UserSerializer
from .permissions import IsUserOwner

from rooms.models import Room
from rooms.serializers import RoomSerializer


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == "list":
            permission_classes = [
                IsAdminUser,
            ]
        elif (
            self.action == "create"
            or self.action == "login"
            or self.action == "retrieve"
        ):
            permission_classes = [
                AllowAny,
            ]
        elif (
            self.action == "me"
            or self.action == "update"
            or self.action == "partial_update"
            or self.action == "toggle_favs"
        ):
            permission_classes = [IsUserOwner]
        elif self.action == "favs":
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsUserOwner]

        return [permissions() for permissions in permission_classes]

    @action(
        detail=False, methods=["get",], permission_classes=[IsAuthenticated,],
    )
    def me(self, request):
        if request.user.is_authenticated:
            serializer = UserSerializer(request.user)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=HTTP_401_UNAUTHORIZED)

    @action(
        detail=False, methods=["post",], permission_classes=[AllowAny,],
    )
    def login(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if user is not None:
            encoded_jwt = jwt.encode(
                {"pk": user.pk}, settings.SECRET_KEY, algorithm="HS256"
            )
            return Response(data={"token": encoded_jwt, "id": user.pk}, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    """
        users/:pk/favs/
        PUT method일 시 pk는 user의 pk가 아니라 room의 pk로 설정해뒀는데, 이게 과연 옳은 방식일지 고민할 필요가 있을듯하다..
        어차피 PUT method 사용시 data가 따로 넘어오는데.. 이럴 필요가 있을까..
    """

    @action(detail=True, methods=["GET",])
    def favs(self, request, pk):
        if request.method == "GET":
            try:
                user = User.objects.get(pk=pk)
                rooms = user.favs.all()
                serialized = RoomSerializer(
                    rooms, many=True, context={"request": request}
                ).data
                return Response(data=serialized, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

    @favs.mapping.put
    def toggle_favs(self, request, pk):
        if pk is not None:
            try:
                room = Room.objects.get(pk=pk)
                user = request.user
                if room in user.favs.all():
                    user.favs.remove(room)
                else:
                    user.favs.add(room)
                return Response(
                    data=RoomSerializer(
                        user.favs.all(), many=True, context={"request": request}
                    ).data,
                    status=status.HTTP_200_OK,
                )
            except Room.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

