from django_filters import rest_framework as filters

from recipes.models import Ingredient, Recipe, Tag


class RecipeFilter(filters.FilterSet):

    is_favorited = filters.BooleanFilter(
        method="filter_is_favorited")
    is_in_shopping_cart = filters.BooleanFilter(
        method="filter_is_in_shopping_cart")
    tags = filters.ModelMultipleChoiceFilter(
        field_name="tags__slug",
        to_field_name="slug",
        queryset=Tag.objects.all(),
    )

    class Meta:
        model = Recipe
        fields = ["is_favorited", "is_in_shopping_cart", "author", "tags"]

    def filter_is_favorited(self, queryset, name, value):
        if value:
            return Recipe.objects.filter(favourite__user=self.request.user)
        return Recipe.objects.all()

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if value:
            return Recipe.objects.filter(purchase__user=self.request.user)
        return Recipe.objects.all()


class IngredientFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Ingredient
        fields = ["name"]
