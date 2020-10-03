from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework import viewsets
from rest_framework.decorators import permission_classes, action
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.status import HTTP_401_UNAUTHORIZED

import jwt

from .models import User
from .serializers import UserSerializer
from .permissions import IsUserOwner


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == "list":
            permission_classes = [
                IsAdminUser,
            ]
        elif self.action == "create" or self.action == "login":
            permission_classes = [
                AllowAny,
            ]
        elif self.action == "retrieve" or self.action == "me":
            permission_classes = [
                IsUserOwner,
            ]
        else:
            permission_classes = [IsUserOwner, IsAdminUser]

        return [permissions() for permissions in permission_classes]

    @action(
        detail=False,
        methods=[
            "get",
        ],
        permission_classes=[
            IsAuthenticated,
        ],
    )
    def me(self, request):
        if request.user.is_authenticated:
            serializer = UserSerializer(request.user)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=HTTP_401_UNAUTHORIZED)

    @action(
        detail=False,
        methods=[
            "post",
        ],
        permission_classes=[
            AllowAny,
        ],
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
            return Response(data={"token": encoded_jwt}, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)