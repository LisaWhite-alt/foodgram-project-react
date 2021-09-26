from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from recipes.models import User, Follow
from .serializers import SubscribeSerializer


@api_view(['GET', 'DELETE'])
def subscribe_detail(request, *args, **kwargs):
    author = get_object_or_404(User, pk=kwargs.get("user_id"))
    subscribe = Follow.objects.filter(user=request.user, author=author)
    if (request.user == author
        or (request.method == "GET" and subscribe.exists())
        or (request.method == "DELETE" and not subscribe.exists())):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "GET" and not subscribe.exists():
        Follow.objects.create(user=request.user, author=author)
        context = {"request": request}
        serializer = SubscribeSerializer(author, context=context)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        subscribe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubscriptionsList(ListAPIView):
    serializer_class = SubscribeSerializer

    def get_queryset(self):
        queryset = User.objects.filter(following__user=self.request.user)
        return queryset
