from rest_framework import viewsets
from rest_framework.decorators import permission_classes, action
from rest_framework import status
from rest_framework.response import Response
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

    @action(detail=False)
    def search(self, request):

        min_price = request.GET.get("min_price", None)
        max_price = request.GET.get("max_price", None)
        beds = request.GET.get("beds", None)
        lat = request.GET.get("lat", None)
        lng = request.GET.get("lng", None)
        bedrooms = request.GET.get("bedrooms", None)
        bathrooms = request.GET.get("bathrooms", None)
        instant_book = request.GET.get("instant_book", None)

        print(min_price)

        filter_kwargs = {}
        if min_price is not None:
            filter_kwargs["price__gte"] = min_price
        if max_price is not None:
            filter_kwargs["price__lte"] = max_price
        if beds is not None:
            filter_kwargs["beds__gte"] = beds
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

        paginator = self.paginator
        paginator.page_size = 10
        try:
            rooms = Room.objects.filter(**filter_kwargs)
        except ValueError:
            return Response(
                data=None,
                status=status.HTTP_400_BAD_REQUEST,
            )
        results = paginator.paginate_queryset(rooms, request)
        serializers = RoomSerializer(results, many=True)

        # return Response(data=serializers.data)
        return paginator.get_paginated_response(serializers.data)
