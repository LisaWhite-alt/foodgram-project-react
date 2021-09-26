from rest_framework.pagination import PageNumberPagination


class RecipeSetPagination(PageNumberPagination):
    page_size = 6
