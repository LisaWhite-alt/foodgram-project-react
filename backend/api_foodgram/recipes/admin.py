from django.contrib import admin
from .models import Ingredient, Tag, Recipe, Follow, Favourite, Purchase


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "measurement_unit",
    )
    search_fields = ("name",)
    list_filter = ("name",)
    empty_value_display = "-пусто-"


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "color",
        "slug",
    )
    search_fields = ("name",)
    empty_value_display = "-пусто-"


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "author",
        "ingredient_names",
        "tag_names",
        "favourite_count",
    )

    def favourite_count(self, obj):
        return Favourite.objects.filter(recipe_id=obj.id).count()
         

    def ingredient_names(self, obj):
        return list(obj.ingredient.all())

    def tag_names(self, obj):
        return list(obj.tag.all())

    search_fields = ("name",)
    list_filter = ("name", "author", "tag")
    empty_value_display = "-пусто-"
    favourite_count.short_description = "Количество попаданий в избранное"
    ingredient_names.short_description = "Ингредиенты"
    tag_names.short_description = "Теги"


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ("user", "author")
    search_fields = ("user__username", "author__username")
    empty_value_display = "-пусто-"


@admin.register(Favourite)
class FavouriteAdmin(admin.ModelAdmin):
    list_display = ("user", "recipe")
    search_fields = ("user__username", "recipe__name")
    empty_value_display = "-пусто-"


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ("user", "recipe")
    search_fields = ("user__username", "recipe__name")
    empty_value_display = "-пусто-"
