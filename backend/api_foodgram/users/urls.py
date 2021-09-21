from django.urls import path, include
# from rest_framework.routers import DefaultRouter

# from .views import MyUserViewSet


# router = DefaultRouter()
# router.register("users", MyUserViewSet, basename="user")

urlpatterns = [
    path("", include('djoser.urls')),
    path("auth/", include('djoser.urls.authtoken')),
    # path("", include(router.urls)),
]
