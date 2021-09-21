"""
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from recipes.models import User
from .serializers import MyUserSerializer



class MyUserViewSet(ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = MyUserSerializer
"""