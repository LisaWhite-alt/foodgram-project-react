from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (IngredientViewSet, RecipeViewSet, TagViewSet,
                    favorite_detail, purchase_detail)

router = DefaultRouter()
router.register("tags", TagViewSet, basename="tag")
router.register("ingredients", IngredientViewSet, basename="ingredient")
router.register("recipes", RecipeViewSet, basename="recipe")

urlpatterns = [
    path("recipes/<int:recipe_id>/favorite/", favorite_detail, name="favorite_detail"),
    path("recipes/<int:recipe_id>/shopping_cart/", purchase_detail, name="purchase_detail"),
    path("", include(router.urls)),
]
