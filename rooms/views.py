import json
from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.decorators import api_view

# from rest_framework.views import APIView
# from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Room
from .serializers import ReadRoomSerializer, TinyRoomSerializer, WriteRoomSerializer


# Create your views here.
"""class ListRoomView(APIView):
    def get(self, request):
        rooms = Room.objects.all()
        rooms_serialized = RoomSerializer(rooms, many=True)
        return Response(data=rooms_serialized.data)"""


"""class ListRoomView(ListAPIView):
    queryset = Room.objects.all()
    serializer_class = TinyRoomSerializer


class SeeRoomView(RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer"""


# old code
"""@api_view(["GET", "POST"])
def room_list(req):
    if req.method == "GET":
        rooms = Room.objects.all()[:5]
        rooms_serialized = ReadRoomSerializer(rooms, many=True)
        return Response(data=rooms_serialized.data)
    elif req.method == "POST":
        if not req.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = WriteRoomSerializer(data=req.data)
        print(serializer.is_valid())
        if serializer.is_valid():
            room = serializer.save(user=req.user)
            room_serialized = ReadRoomSerializer(room).data
            return Response(data=room_serialized, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)"""


class RoomListView(APIView):
    def get(self, request):
        rooms = Room.objects.all()[:5]
        rooms_serialized = ReadRoomSerializer(rooms, many=True)
        return Response(data=rooms_serialized.data)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = WriteRoomSerializer(data=request.data)

        if serializer.is_valid():
            room = serializer.save(user=request.user)
            room_serialized = ReadRoomSerializer(room).data
            return Response(data=room_serialized, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoomDetailView(APIView):
    def get_room(self, pk):
        try:
            room = Room.objects.get(pk=pk)
            return room
        except Room.DoesNotExist:
            return None

    def get(self, request, pk):

        room = self.get_room(pk)

        if room is not None:
            room_serialized = ReadRoomSerializer(room)
            return Response(data=room_serialized.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        room = self.get_room(pk)

        if room is not None:
            if room.user != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            print(request.data)
            room_serialized = WriteRoomSerializer(room, data=request.data, partial=True)
            if room_serialized.is_valid():
                room = room_serialized.save()
                return Response(
                    data=ReadRoomSerializer(room).data, status=status.HTTP_200_OK
                )
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        room = self.get_room(pk)

        if room is not None:
            if room.user == request.user:
                room.delete()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)

        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


"""@api_view(["GET", "POST"])
def room_detail(req, pk):
    room = Room.objects.get(pk=pk)
    room_serialized = ReadRoomSerializer(room)

    return Response(data=room_serialized.data)"""


"""def room_list(req):
    data = serializers.serialize("json", Room.objects.all())

    response = HttpResponse(content=data,)

    return response"""
