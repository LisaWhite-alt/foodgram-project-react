from rest_framework import serializers

from .models import Tag, Ingredient, IngredientAmount, Recipe, Follow, User, Favourite, Purchase

from drf_extra_fields.fields import Base64ImageField


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
        representation = super().to_representation(instance)
        data = {
            "id": representation["ingredient"]["id"],
            "name": representation["ingredient"]["name"],
            "measurement_unit": representation["ingredient"]["measurement_unit"],
            "amount": representation["amount"]
        }
        return data

class IngredientAmountPostSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    def validate_id(self, value):
        if value < 1:
            raise serializers.ValidationError()
        return value

    def validate_amount(self, value):
        if value < 1:
            raise serializers.ValidationError()
        return value


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

class RecipeListSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    author = UserSerializer(read_only=True)
    ingredients = IngredientAmountListSerializer(source="ingredientamount_set",many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    # image = Base64ImageField(max_length=None, use_url=True)

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
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)
    ingredients = IngredientAmountPostSerializer(many=True)
    name = serializers.CharField(max_length=200)
    image = Base64ImageField()
    text = serializers.CharField()
    cooking_time = serializers.IntegerField()

    def create(self, validated_data):
        ingredients = validated_data.pop("ingredients")
        tags = validated_data.pop("tags")
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        for item in ingredients:
            current_ingredient = Ingredient.objects.get(pk=item["id"])
            IngredientAmount.objects.create(
                    recipe=recipe,
                    amount=item["amount"],
                    ingredient=current_ingredient
                )
        return recipe
    
    def validate_cooking_time(self, value):
        if value < 1:
            raise serializers.ValidationError()
        return value

    def to_representation(self, instance):
        return RecipeListSerializer(instance, context=self.context).data



"""
    def update(self, instance, validated_data):
        contents = validated_data.pop('contents')
        tags = validated_data.pop('tags')
        instance.tags.set(tags)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        instance.ingredients.clear()
        for item in contents:
            content = ContentSerializer(item).data
            amount = content['amount']
            ingredient_id = content['id']
            ingredient = Ingredient.objects.get(pk=ingredient_id)
            content = Content.objects.create(
                recipe=instance,
                ingredient=ingredient, amount=amount
            )
            content.save()
        return instance
"""

class RecipeMinifiedSerializer(serializers.ModelSerializer):
    # image = serializers.HyperlinkedRelatedField(many=True, view_name="recipe", read_only=True, lookup_field="recipe")

    class Meta:
        fields = (
            "id",
            "name",
            "image",
            "cooking_time"
        )
        model = Recipe
