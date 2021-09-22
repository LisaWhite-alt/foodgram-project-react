from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from recipes.models import User, Follow
from .serializers import SubscribeSerializer


@api_view(['GET', 'DELETE'])
def subscribe_detail(request, *args, **kwargs):
    context = {"request": request}
    author = get_object_or_404(User, pk=kwargs.get("user_id"))
    if request.method == 'GET':
        serializer = SubscribeSerializer(author, context=context)
        Follow.objects.create(user=request.user, author=author)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    subscribe = Follow.objects.filter(user=request.user, author=author)
    if subscribe.exists():
        subscribe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_400_BAD_REQUEST)
