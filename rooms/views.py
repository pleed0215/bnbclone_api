import json
from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponse

from .models import Room


# Create your views here.


def room_list(req):
    data = serializers.serialize("json", Room.objects.all())

    response = HttpResponse(content=data,)

    return response
