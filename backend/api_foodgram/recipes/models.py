from colorfield.fields import ColorField
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models


class User(AbstractUser):
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name="Электронная почта",
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="Логин",
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name="Имя",
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name="Фамилия",
    )
    password = models.CharField(
        max_length=150,
        verbose_name="Пароль",
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username


class Ingredient(models.Model):
    name = models.CharField(
        "Название ингредиента",
        max_length=80
    )
    measurement_unit = models.CharField(
        "Единица измерения",
        max_length=20
    )

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        "Название тега",
        max_length=50
    )
    color = ColorField(
        default="#FF0000",
        verbose_name="Цвет"
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
        upload_to="images",
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
        User,
        db_column="author",
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="Автор рецепта"
    )
    pub_date = models.DateTimeField(
        "Дата публикации",
        auto_now_add=True
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through="IngredientAmount",
        verbose_name="Ингредиенты"
    )
    tags = models.ManyToManyField(
        Tag,
        related_name="tags",
        verbose_name="Теги"
    )

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        ordering = ["-pub_date"]

    def __str__(self):
        return f"Рецепт {self.name} от {self.author}"


class IngredientAmount(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name="Ингредиент"
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )
    amount = models.PositiveSmallIntegerField(
        "Количество ингредиента",
        validators=[
            MinValueValidator(
                1,
                message="Минимальное количество ингредиента: 1 единица"
            ),
        ],
    )


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower",
        verbose_name="Кто подписался"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following",
        verbose_name="На кого подписались"
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "author"],
                name="unique_follow"
            ),
        ]

    def __str__(self):
        return f"Пользователь {self.user} подписан на {self.author}"


class Favourite(models.Model):
    user = models.ForeignKey(
        User,
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
        User,
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
