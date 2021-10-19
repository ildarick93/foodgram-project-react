from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.serializers import RecipeLiteSerializer

from .filters import CustomSearchFilter, RecipeFilter
from .models import (FavoriteRecipe, Ingredient, IngredientAmountInRecipe,
                     Recipe, ShoppingList, Tag)
from .permissions import OwnerOrAdminOrAuthenticatedOrReadOnly
from .serializers import (CreateUpdateRecipeSerializer, IngredientSerializer,
                          RecipeSerializer, TagSerializer)
from .utils import add_file_to_response, form_shop_list


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = [CustomSearchFilter]
    search_fields = ['^name']


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    filterset_class = RecipeFilter
    serializer_class = RecipeSerializer  # full
    permission_classes = [OwnerOrAdminOrAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def _create_link(self, request, model):
        object = get_object_or_404(Recipe, pk=self.kwargs['pk'])
        user = request.user
        existance = model.objects.filter(user=user, recipe=object).exists()
        if not existance:
            model.objects.create(user=user, recipe=object)
            serializer = RecipeLiteSerializer(object)  # lite
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            raise ValidationError({'errors': 'Already exists'})

    def _delete_link(self, request, model):
        user = request.user
        model.objects.filter(user=user, recipe__pk=self.kwargs['pk']).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def favorite(self, request, *args, **kwargs):
        return self._create_link(request, FavoriteRecipe)

    @favorite.mapping.delete
    def delete_favorite(self, request, *args, **kwargs):
        return self._delete_link(request, FavoriteRecipe)

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, *args, **kwargs):
        return self._create_link(request, ShoppingList)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, *args, **kwargs):
        return self._delete_link(request, ShoppingList)

    @action(
        methods=['get'],
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request, *args, **kwargs):
        results = IngredientAmountInRecipe.objects.filter(
            recipe__is_in_shopping_list__user=request.user
        ).select_related('recipe').select_related('ingredient')
        data = form_shop_list(results)
        return add_file_to_response(data, 'text/plain')

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update']:
            return CreateUpdateRecipeSerializer
        return RecipeSerializer
