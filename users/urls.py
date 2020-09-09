from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("me/", views, name="me"),
    path("<int:pk>", views, name="profile"),
]
