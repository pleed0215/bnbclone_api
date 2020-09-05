import json
from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponse

#from rest_framework.decorators import api_view
#from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from .models import Room
from .serializers import RoomSerializer, TinyRoomSerializer


# Create your views here.
"""class ListRoomView(APIView):
    def get(self, request):
        rooms = Room.objects.all()
        rooms_serialized = RoomSerializer(rooms, many=True)
        return Response(data=rooms_serialized.data)"""

class ListRoomView(ListAPIView):
    queryset = Room.objects.all()
    serializer_class = TinyRoomSerializer

class SeeRoomView(RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

# old code
"""@api_view(["GET"])
def room_list(req):
    rooms = Room.objects.all()
    rooms_serialized = RoomSerializer(rooms, many=True)
    return Response(data=rooms_serialized.data)"""


"""def room_list(req):
    data = serializers.serialize("json", Room.objects.all())

    response = HttpResponse(content=data,)

    return response"""
