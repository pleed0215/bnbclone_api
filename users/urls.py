from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("me/", views.MeView.as_view(), name="me"),
    path("me/fav", views.toggle_fav_view, name="fav"),
    path("<int:pk>/", views.user_detail, name="profile"),
]
