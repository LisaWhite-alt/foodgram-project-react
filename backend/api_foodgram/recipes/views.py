from django.shortcuts import get_object_or_404

from rest_framework import filters, permissions, status
from rest_framework.decorators import api_view
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from .filters import RecipeFilter
from .models import Tag, Ingredient, Recipe, Favourite, Purchase
from .serializers import TagSerializer, IngredientSerializer, RecipeListSerializer, RecipePostSerializer, RecipeMinifiedSerializer
from .pagination import RecipeSetPagination


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("^name",)


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filter_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user
        )
    
    def get_serializer_class(self):
        if self.request.method in ["POST", "PUT"]:
            return RecipePostSerializer
        return RecipeListSerializer


@api_view(['GET', 'DELETE'])
def favorite_detail(request, *args, **kwargs):
    recipe = get_object_or_404(Recipe, pk=kwargs.get("recipe_id"))
    favorite = Favourite.objects.filter(user=request.user, recipe=recipe)
    if ((request.method == "GET" and favorite.exists())
        or (request.method == "DELETE" and not favorite.exists())):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "GET" and not favorite.exists():
        Favourite.objects.create(user=request.user, recipe=recipe)
        context = {"request": request}
        serializer = RecipeMinifiedSerializer(recipe, context=context)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'DELETE'])
def purchase_detail(request, *args, **kwargs):
    recipe = get_object_or_404(Recipe, pk=kwargs.get("recipe_id"))
    purchase = Purchase.objects.filter(user=request.user, recipe=recipe)
    if ((request.method == "GET" and purchase.exists())
        or (request.method == "DELETE" and not purchase.exists())):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "GET" and not purchase.exists():
        Purchase.objects.create(user=request.user, recipe=recipe)
        context = {"request": request}
        serializer = RecipeMinifiedSerializer(recipe, context=context)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        purchase.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def download_shopping_cart(request):
    recipes = Recipe.objects.filter(purchase__user=self.request.user)
    purchase_list = []
    for recipe in recipes:
        for item in recipe.ingredients:
            name = item__ingredient__name
            measurement_unit = item__ingredient__measurement_unit
            amount = item_amount
            for element in purchase_list:
                if name not in element:
                    purchase_list.append([name, measurement_unit, amount])
                else:
                    element[2] += amount

