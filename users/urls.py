from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views
from . import viewsets

app_name = "users"

router = DefaultRouter()
router.register("", viewsets.UsersViewSet, basename="users")
urlpatterns = router.urls

"""
urlpatterns = [
    path("", views.UsersView.as_view(), name="create"),
    path("auth/", views.login, name="login"),
    path("me/", views.MeView.as_view(), name="me"),
    path("me/favs/", views.FavsView.as_view(), name="favs"),
    path("<int:pk>/", views.user_detail, name="profile"),
]
"""