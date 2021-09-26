from rest_framework import filters, permissions
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from .models import Tag, Ingredient, Recipe
from .serializers import TagSerializer, IngredientSerializer, RecipeListSerializer, RecipePostSerializer
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
    pagination_class = RecipeSetPagination

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user
        )
    
    def get_serializer_class(self):
        if self.request.method in ["POST", "PUT"]:
            return RecipePostSerializer
        return RecipeListSerializer
