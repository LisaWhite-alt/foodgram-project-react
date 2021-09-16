from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

USER = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(
        "Название ингредиента",
        max_length=80,
        db_index=True
    )
    measurement_unit = models.CharField(
        "Единица измерения",
        max_length=20
    )
    amount = models.PositiveSmallIntegerField(
        "Количество ингредиента",
        default=1,
        validators=[
            MinValueValidator(
                1,
                message="Минимальное количество ингредиента: 1 единица"
            ),
        ],
    )

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        "Название тега",
        max_length=50,
        db_index=True
    )
    color = ColorField(
        default="#FF0000"
    )
    slug = models.SlugField(
        max_length=50,
        unique=True
    )
    
    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(
        "Название рецепта",
        max_length=200
    )
    text = models.TextField(
        "Текст рецепта",
    )
    image = models.ImageField(
        upload_to="static/images",
        verbose_name="Изображение"
    )
    cooking_time = models.PositiveSmallIntegerField(
        "Время приготовления (в минутах)",
        validators=[
            MinValueValidator(
                1,
                message="Минимальное время приготовления: 1 минута"
            ),
        ],
    )
    author = models.ForeignKey(
        USER,
        db_column="author",
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="Автор рецепта"
    )
    pub_date = models.DateTimeField(
        "Дата публикации",
        auto_now_add=True
    )
    ingredient = models.ManyToManyField(
        Ingredient,
        related_name="ingredient",
        verbose_name="Ингредиент",
    )
    tag = models.ManyToManyField(
        Tag,
        related_name="tag",
        verbose_name="Тег"
    )

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        ordering = ["-pub_date"]

    def __str__(self):
        return f"Рецепт {self.name} от {self.author}"


class Follow(models.Model):
    user = models.ForeignKey(
        USER,
        on_delete=models.CASCADE,
        related_name="follower",
        verbose_name="Кто подписался"
    )
    author = models.ForeignKey(
        USER,
        on_delete=models.CASCADE,
        related_name="following",
        verbose_name="На кого подписались"
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self):
        return f"Пользователь {self.user} подписан на {self.author}"



class Favourite(models.Model):
    user = models.ForeignKey(
        USER,
        on_delete=models.CASCADE,
        related_name="elector",
        verbose_name="Кто выбрал рецепт"
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="favourite",
        verbose_name="Выбранный рецепт"
    )

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранные"

    def __str__(self):
        return f"Пользователь {self.user} выбрал {self.recipe}"


class Purchase(models.Model):
    user = models.ForeignKey(
        USER,
        on_delete=models.CASCADE,
        related_name="buyer",
        verbose_name="Покупатель"
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="purchase",
        verbose_name="Рецепт для покупки"
    )

    class Meta:
        verbose_name = "Покупка"
        verbose_name_plural = "Покупки"

    def __str__(self):
        return f"Пользователь {self.user} выбрал к покупке {self.recipe}"
