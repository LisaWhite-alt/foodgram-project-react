from django.urls import path, include
from .views import SubscriptionsList, subscribe_detail


urlpatterns = [
    path("users/<int:user_id>/subscribe/", subscribe_detail, name="subscribe_detail"),
    path("users/subscriptions/", SubscriptionsList.as_view()),
    path("", include('djoser.urls')),
    path("auth/", include('djoser.urls.authtoken')),
]
