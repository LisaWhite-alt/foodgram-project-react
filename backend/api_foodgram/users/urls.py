from django.urls import path, include
from .views import subscribe_detail


urlpatterns = [
    path("users/<int:user_id>/subscribe/", subscribe_detail, name="subscribe_detail"),
    path("", include('djoser.urls')),
    path("auth/", include('djoser.urls.authtoken')),
]
