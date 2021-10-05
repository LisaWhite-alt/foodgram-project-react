from django_filters import filters
from django_filters.rest_framework import FilterSet

from .models import Ingredient, Recipe


class RecipeFilter(FilterSet):

    is_favorited = filters.ModelChoiceFilter(
        lookup_expr="isnull",
        queryset=Recipe.objects.all(),
        method="filter_is_favorited",
    )
    is_in_shopping_cart = filters.ModelChoiceFilter(
        lookup_expr="isnull",
        queryset=Recipe.objects.all(),
        method="filter_is_in_shopping_cart",
    )
    author = filters.AllValuesFilter(field_name="author")
    tags = filters.AllValuesMultipleFilter(field_name="tags__slug")

    class Meta:
        model = Recipe
        fields = ["is_favorited", "is_in_shopping_cart", "author", "tags"]

    def filter_is_favorited(self, queryset, name, value):
        return queryset.filter(favourite__user=self.request.user)

    def filter_is_in_shopping_cart(self, queryset, name, value):
        return queryset.filter(purchase__user=self.request.user)


class IngredientFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Ingredient
        fields = ["name"]
