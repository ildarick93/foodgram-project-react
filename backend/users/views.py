from django.contrib.auth import get_user_model
from django.db.models import Count
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .models import Subscription
from .serializers import CustomUserSerializer, SubscriptionsSerializer

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    serializer_class = CustomUserSerializer

    @action(detail=False, methods=('GET',))
    def subscriptions(self, request):
        user = self.request.user
        subscribed_to = user.subscribed_to.all().values_list(
            'subscribed_to_id', flat=True)
        queryset = User.objects.filter(id__in=subscribed_to).annotate(
            count=Count('recipes__id'))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = SubscriptionsSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = SubscriptionsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=('GET',))
    def subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, id=id)
        if user.id == id:
            raise ValidationError('You can not subscribe to yourself')
        if int(id) in user.subscribed_to.all().values_list(
                'subscribed_to', flat=True):
            raise ValidationError('You already follow this author')
        else:
            follow = Subscription.objects.create(
                subscriber=user,
                subscribed_to=author
            )
            follow.save()
            serializer = SubscriptionsSerializer(author)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def delete_subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, id=id)
        follow = get_object_or_404(
            Subscription,
            subscriber=user,
            subscribed_to=author)
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == 'subscriptions':
            user = self.request.user
            subscribed_to = user.subscribed_to.all().values_list(
                'subscribed_to_id', flat=True)
            queryset = User.objects.filter(id__in=subscribed_to).annotate(
                count=Count('recipes__id'))
            return queryset
        return queryset
