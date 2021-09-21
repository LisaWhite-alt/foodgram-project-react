from rest_framework import serializers
from djoser.serializers import UserCreateSerializer, UserSerializer
from recipes.models import Follow


class UserRegistrationSerializer(UserCreateSerializer):

    class Meta(UserCreateSerializer.Meta):
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "password"
        ) 


class MyUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "is_subscribed", 
        ) 
    
    def get_is_subscribed(self, obj):
        if obj == self.context["request"].user:
            return "true"
        return Follow.objects.filter(user=self.context["request"].user, author=obj).exists()
