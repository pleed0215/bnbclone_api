import json
from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination

# from rest_framework.views import APIView
# from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Room
from .serializers import (
    ReadRoomSerializer,
    TinyRoomSerializer,
    WriteRoomSerializer,
    RoomSerializer,
)


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
        paginator = PageNumberPagination()
        paginator.page_size = 20
        rooms = Room.objects.all()
        result = paginator.paginate_queryset(rooms, request)
        rooms_serialized = RoomSerializer(
            result, many=True, context={"request": request}
        )
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


@api_view(["GET"])
def room_search(request):

    min_price = request.GET.get("min_price", None)
    max_price = request.GET.get("max_price", None)
    beds = request.GET.get("beds", None)
    lat = request.GET.get("lat", None)
    lng = request.GET.get("lng", None)
    bedrooms = request.GET.get("bedrooms", None)
    bathrooms = request.GET.get("bathrooms", None)
    instant_book = request.GET.get("instant_book", None)

    filter_kwargs = {}
    if min_price is not None:
        filter_kwargs["price__gte"] = min_price
    if max_price is not None:
        filter_kwargs["price__lte"] = max_price
    if beds is not None:
        filter["beds__gte"] = beds
    if lat is not None and lng is not None:
        filter_kwargs["lat__gte"] = float(lat) - 0.005
        filter_kwargs["lat__lte"] = float(lat) + 0.005
        filter_kwargs["lng__gte"] = float(lng) - 0.005
        filter_kwargs["lng__lte"] = float(lng) + 0.005
    if bedrooms is not None:
        filter_kwargs["bedrooms__gte"] = bedrooms
    if bathrooms is not None:
        filter_kwargs["bathrooms__gte"] = bathrooms
    if instant_book is not None:
        filter_kwargs["instant_book__gte"] = instant_book

    paginator = PageNumberPagination()
    paginator.page_size = 10
    try:
        rooms = Room.objects.filter(**filter_kwargs)
    except ValueError:
        return Response(
            data=None,
            status=status.HTTP_400_BAD_REQUEST,
        )
    results = paginator.paginate_queryset(rooms, request)
    serializers = ReadRoomSerializer(results, many=True)

    # return Response(data=serializers.data)
    return paginator.get_paginated_response(serializers.data)
