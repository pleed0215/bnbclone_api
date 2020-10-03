from rest_framework import viewsets
from rest_framework.decorators import permission_classes, action
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.status import HTTP_401_UNAUTHORIZED
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
        elif self.action == "create":
            permission_classes = [
                AllowAny,
            ]
        elif self.action == "retrieve":
            permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            permission_classes = [IsUserOwner, IsAdminUser]

        return [permissions() for permissions in permission_classes]

    @action(
        detail=False,
        url_path="me/",
        methods=[
            "get",
        ],
        permission_classes=[
            IsAuthenticated,
        ],
    )
    def user_detail(self, request):
        if request.user.is_authenticated:
            serializer = UserSerializer(data=request.user)
            return Response(data=serializer, status=status.HTTP_200_OK)
        else:
            return Response(status=HTTP_401_UNAUTHORIZED)