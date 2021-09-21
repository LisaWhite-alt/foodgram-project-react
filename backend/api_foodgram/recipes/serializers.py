from rest_framework import serializers

from .models import Tag, Ingredient, IngredientAmount, Recipe, Follow, User, Favourite


class UserSerializer(serializers.ModelSerializer):
    # is_subscribed = serializers.SerializerMethodField()

    class Meta:
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            # "is_subscribed"
        )
        model = User
"""
    def get_is_subscribed(self, obj):
        return Follow.objects.filter(
            user=self.context["request"].user, author=obj).exists()
"""

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Tag


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Ingredient


class IngredientAmountSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            "ingredient",
            "amount"
        )
        model = IngredientAmount

"""
class Base64(serializers.Field):
    def to_representation(self, value):
        return value
    def to_internal_value(self, data):
        try:
            data = Base64ImageField(data)
        except ValueError:
            raise serializers.ValidationError("Не получается конвертировать картинку")
        return data
"""

class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    ingredients = IngredientAmountSerializer(source="ingredientamount_set",many=True, read_only=True)
    # is_favorited = serializers.SerializerMethodField()
    # is_in_shopping_cart = serializers.SerializerMethodField()
    # image = Base64ImageField(represent_in_base64=True)

    class Meta:
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            # "is_favorited",
            # "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time"
        )
        model = Recipe
"""
    def get_is_favorited(self, obj):
        if self.context["request"].user.id == settings.ANONYMOUS_USER_ID:
            return False
        return Favourite.objects.filter(
            user=self.context["request"].user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        return Purchase.objects.filter(
            user=self.context["request"].user, recipe=obj).exists()
"""