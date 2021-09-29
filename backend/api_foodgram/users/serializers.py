from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from recipes.models import Follow, Recipe
from recipes.serializers import RecipeMinifiedSerializer


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
            return True
        return Follow.objects.filter(user=self.context["request"].user, author=obj).exists()



class SubscribeSerializer(MyUserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta(MyUserSerializer.Meta):
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            "recipes_count"
        )

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()

    def get_recipes(self, obj):
        limit = 6
        try:
            limit = self.context["request"].query_params["recipes_limit"]
        except Exception:
            pass
        queryset = Recipe.objects.filter(author=obj)[:int(limit)]
        serializer = RecipeMinifiedSerializer(queryset, context=self.context, many=True)
        return serializer.data
