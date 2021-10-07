import io

from django.db.models import Sum
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.serializers import RecipeLiteSerializer

from .filters import CustomSearchFilter, RecipeFilter
from .models import FavoriteRecipe, Ingredient, Recipe, ShoppingList, Tag
from .permissions import IsAdmin, IsOwner, ReadOnly
from .serializers import IngredientSerializer, RecipeSerializer, TagSerializer


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
    permission_classes = [IsOwner | IsAdmin | IsAuthenticated | ReadOnly]

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

    @action(detail=False, methods=['get'])
    def download_shopping_cart(self, request):
        queryset = ShoppingList.objects.filter(
            user_id=self.request.user).values(
            'recipe_id__ingredients__name',
            'recipe_id__ingredients__measurements_unit').annotate(
                Sum('recipe_id__ingredientamountinrecipe__amount'))
        buffer = get_pdf_file(queryset)
        return FileResponse(buffer, as_attachment=True, filename='hello.pdf')


def get_pdf_file(queryset):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    p.setLineWidth(.3)
    pdfmetrics.registerFont(TTFont('FreeSans', 'FreeSans.ttf'))
    p.setFont('FreeSans', 14)
    t = p.beginText(30, 750, direction=0)
    t.textLine('Shopping list')
    p.line(30, 747, 580, 747)
    t.textLine(' ')
    for qs in queryset:
        title = qs['recipe_id__ingredients__name']
        amount = qs['recipe_id__ingredients_amount__amount__sum']
        measurements_unit = qs['recipe_id__ingredients__measurements_unit']
        t.textLine(f'{title} ({measurements_unit}) - {amount}')
    p.drawText(t)
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer
