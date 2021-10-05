from collections import defaultdict

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .filters import IngredientFilter, RecipeFilter
from .models import Favourite, Ingredient, Purchase, Recipe, Tag
from .serializers import (IngredientSerializer, RecipeListSerializer,
                          RecipeMinifiedSerializer, RecipePostSerializer,
                          TagSerializer)


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = IngredientFilter
    pagination_class = None


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user
        )

    def get_serializer_class(self):
        if self.request.method in ["POST", "PUT"]:
            return RecipePostSerializer
        return RecipeListSerializer

    @action(detail=False, url_path="download_shopping_cart")
    def download_shopping_cart(self, request):
        recipes = Recipe.objects.values_list(
            "ingredientamount__ingredient__name",
            "ingredientamount__ingredient__measurement_unit",
            "ingredientamount__amount"
        ).filter(purchase__user=self.request.user)
        content = defaultdict(int)
        for item in recipes:
            content[item[0] + " (" + item[1] + ") - "] += item[2]
        pdfmetrics.registerFont(TTFont(
            'DejaVuSerif',
            'DejaVuSerif.ttf',
            'UTF-8'
        ))
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = (
            'attachment; filename="shopping_cart.pdf"')
        page = canvas.Canvas(response)
        x = 50
        y = 800
        page.setFont('DejaVuSerif', size=15)
        page.drawString(x, y, "Список покупок:")
        page.setFont('DejaVuSerif', size=10)
        y = y - 50
        for item in content:
            page.drawString(x, y, item + str(content[item]))
            y = y - 30
        page.showPage()
        page.save()
        return response


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
