from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.authentication import (SessionAuthentication,
                                           TokenAuthentication)
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .models import Subscription
from .serializers import CustomUserSerializer, SubscriptionsSerializer

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    @action(
        methods=('GET'),
        detail=False,
        serializer_class=SubscriptionsSerializer,
    )
    def subscriptions(self, request, *args, **kwargs):
        subscriptions = User.objects.filter(
            following__user=self.request.user
        )
        page = self.paginate_queryset(subscriptions)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=('GET'),
    )
    def subscribe(self, request, *args, **kwargs):
        subscribed_to = get_object_or_404(User, id=self.kwargs['id'])
        existance = Subscription.objects.filter(
            subscriber=request.user,
            subscribed_to=subscribed_to
        ).exists()
        if request.user == subscribed_to:
            raise ValidationError(
                {"errors": "It's not allowed to subscribe on youself"}
            )
        if not existance:
            Subscription.objects.create(
                subscriber=request.user,
                subscribed_to=subscribed_to
            )
            serializer = CustomUserSerializer(
                subscribed_to,
                context={'request': request}
            )
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        else:
            raise ValidationError(
                {"errors": "Such subscription already exists"}
            )

    @subscribe.mapping.delete
    def unsubscribe(self, request, *args, **kwargs):
        Subscription.objects.filter(
            subscriber=request.user,
            subscribed_to__id=self.kwargs['id']
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
