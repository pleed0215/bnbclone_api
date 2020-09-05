from django.urls import path

# from rest_framework.routers import DefaultRouter

from . import views

# from . import viewsets

app_name = "rooms"

"""router = DefaultRouter()
router.register ("", viewsets.RoomViewset, basename="room")

urlpatterns = router.urls"""


# due to use viewset, re-write this part, above.
urlpatterns = [
    path(
        "list/",
        views.room_list,
    ),
    path("<int:pk>/", views.room_detail),
]
