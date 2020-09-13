from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .serializers import UserSerializer, FavsSerializer
from .models import User
from rooms.models import Room
from rooms.serializers import RoomSerializer


class UsersView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serialized = serializer.save()
            return Response(
                data=UserSerializer(serialized).data, status=status.HTTP_200_OK
            )
        else:
            return Response(seriailzer.error, status=status.HTTP_400_BAD_REQUEST)


# Create your views here.
class MeView(APIView):

    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request):
        return Response(
            data=UserSerializer(request.user,).data, status=status.HTTP_200_OK,
        )

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            updated = serializer.save()
            return Response(
                data=UserSerializer(updated).data, status=status.HTTP_200_OK
            )
        else:
            return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def user_detail(request, pk):
    try:
        requested = User.objects.get(pk=pk)
        return Response(
            data=ReadUserSerializer(requested).data, status=status.HTTP_200_OK
        )
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


class FavsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        rooms = user.favs.all()
        serialized = RoomSerializer(rooms, many=True).data
        return Response(data=serialized, status=status.HTTP_200_OK)

    def put(self, request):
        pk = request.data.get("pk")
        if pk is not None:
            try:
                room = Room.objects.get(pk=pk)
                user = request.user
                if room in user.favs.all():
                    user.favs.remove(room)
                else:
                    user.favs.add(room)
                return Response(
                    data=RoomSerializer(user.favs.all(), many=True).data,
                    status=status.HTTP_200_OK,
                )
            except Room.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
