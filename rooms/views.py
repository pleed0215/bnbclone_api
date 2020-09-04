import json
from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Room
from .serializers import RoomSerializer


# Create your views here.

@api_view(["GET"])
def room_list(req):
    rooms = Room.objects.all()
    rooms_serialized = RoomSerializer(rooms, many=True)
    return Response(data=rooms_serialized.data)


"""def room_list(req):
    data = serializers.serialize("json", Room.objects.all())

    response = HttpResponse(content=data,)

    return response"""
