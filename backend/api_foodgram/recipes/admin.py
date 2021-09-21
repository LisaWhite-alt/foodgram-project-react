from django.contrib import admin
from .models import (Ingredient, Tag, Recipe, Follow, Favourite,
                     Purchase, IngredientAmount, User)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
    )
    search_fields = ("email",)
    list_filter = ("username", "email", "first_name")
    empty_value_display = "-пусто-"


class IngredientAmountInline(admin.TabularInline):
    model = IngredientAmount
    extra = 1


class TagInline(admin.TabularInline):
    model = Recipe.tags.through
    extra = 1


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
    inlines = [
        TagInline,
        IngredientAmountInline
    ]
    exclude = ("tags",)
    list_display = (
        "pk",
        "name",
        "author",
        "favourite_count",
    )

    def favourite_count(self, obj):
        return Favourite.objects.filter(recipe_id=obj.id).count()

    search_fields = ("name",)
    list_filter = ("name", "author", "tags")
    empty_value_display = "-пусто-"
    favourite_count.short_description = "Количество попаданий в избранное"


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
