from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from users.models import User

from .models import (Favourite, Follow, Ingredient, IngredientAmount, Purchase,
                     Recipe, Tag)


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed"
        )
        model = User

    def get_is_subscribed(self, obj):
        user = self.context["request"].user
        return not user.is_anonymous and (Follow.objects.filter(
            user=user, author=obj
        ).exists() or user == obj)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Tag


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Ingredient


class IngredientAmountListSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer()

    class Meta:
        fields = (
            "ingredient",
            "amount"
        )
        model = IngredientAmount

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        return {
            "id": rep["ingredient"]["id"],
            "name": rep["ingredient"]["name"],
            "measurement_unit": rep["ingredient"]["measurement_unit"],
            "amount": rep["amount"]
        }


class IngredientAmountPostSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField()


class RecipeListSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    author = UserSerializer(read_only=True)
    ingredients = IngredientAmountListSerializer(
        source="ingredientamount_set",
        many=True
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time"
        )
        model = Recipe

    def get_is_favorited(self, obj):
        user = self.context["request"].user
        return not user.is_anonymous and Favourite.objects.filter(
            user=user, recipe=obj
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context["request"].user
        return not user.is_anonymous and Purchase.objects.filter(
            user=user, recipe=obj
        ).exists()


class RecipePostSerializer(serializers.Serializer):
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    ingredients = IngredientAmountPostSerializer(many=True)
    name = serializers.CharField(max_length=200)
    image = Base64ImageField(max_length=None, use_url=True)
    text = serializers.CharField()
    cooking_time = serializers.IntegerField()

    def validate(self, data):
        if not data['ingredients']:
            raise serializers.ValidationError(
                "В рецепте должен быть хотя бы один ингредиент")
        list_id = []
        for item in data['ingredients']:
            if item["id"] < 1:
                raise serializers.ValidationError(
                    "id ингредиента должно быть больше 0")
            elif item["id"] in list_id:
                raise serializers.ValidationError(
                    "В рецепте не должно быть одинаковых ингредиентов")
            elif item["amount"] < 1:
                raise serializers.ValidationError(
                    "Количество ингредиента должно быть больше 0")
            list_id.append(item["id"])
        if data['cooking_time'] < 1:
            raise serializers.ValidationError(
                "Время приготовления должно быть больше 0")
        return data

    def to_representation(self, instance):
        return RecipeListSerializer(instance, context=self.context).data

    def create_ingredient_amount(self, ingredients, value):
        for item in ingredients:
            current_ingredient = Ingredient.objects.get(pk=item["id"])
            IngredientAmount.objects.create(
                recipe=value,
                amount=item["amount"],
                ingredient=current_ingredient
            )
        return value

    def create(self, validated_data):
        ingredients = validated_data.pop("ingredients")
        tags = validated_data.pop("tags")
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.create_ingredient_amount(ingredients, recipe)
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop("ingredients")
        tags = validated_data.pop("tags")
        instance.name = validated_data.get("name", instance.name)
        instance.image = validated_data.get("image", instance.image)
        instance.text = validated_data.get("text", instance.text)
        instance.cooking_time = validated_data.get(
            "cooking_time", instance.cooking_time)
        instance.tags.set(tags)
        instance.save()
        instance.ingredients.clear()
        self.create_ingredient_amount(ingredients, instance)
        return instance


class RecipeMinifiedSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            "id",
            "name",
            "image",
            "cooking_time"
        )
        model = Recipe
