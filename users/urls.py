from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("", views.UsersView.as_view(), name="create"),
    path("me/", views.MeView.as_view(), name="me"),
    path("me/favs/", views.FavsView.as_view(), name="favs"),
    path("<int:pk>/", views.user_detail, name="profile"),
]
