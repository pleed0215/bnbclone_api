from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .serializers import ReadUserSerializer, WriteUserSerializer
from .models import User

# Create your views here.
class MeView(APIView):

    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request):
        return Response(
            data=ReadUserSerializer(
                request.user,
            ).data,
            status=status.HTTP_200_OK,
        )

    def put(self, request):
        serializer = WriteUserSerializer(request.data, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
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