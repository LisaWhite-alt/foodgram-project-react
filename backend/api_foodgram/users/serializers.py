from djoser.serializers import UserCreateSerializer, UserSerializer
from recipes.models import Follow, Recipe
from recipes.serializers import RecipeMinifiedSerializer
from rest_framework import serializers


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
        user = self.context["request"].user
        return not user.is_anonymous and (Follow.objects.filter(
            user=user, author=obj
        ).exists() or user == obj)


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

    def validate(self, value):
        if value < 1 or value is not int:
            raise ValueError()
        return value

    def get_recipes(self, obj):
        try:
            limit = self.context["request"].query_params["recipes_limit"]
            self.validate(limit)
        except Exception:
            limit = 6
        queryset = Recipe.objects.filter(author=obj)[:int(limit)]
        serializer = RecipeMinifiedSerializer(
            queryset,
            context=self.context,
            many=True
        )
        return serializer.data
