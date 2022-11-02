from reviews.models import Category, Genre, Title

from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny

from .permissions import IsAdmin, IsAdminOrReadOnly, IsAdminModeratirAuthor
from .serializers import (CategorySerializer, GenreSerializer, TitleSerializer)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = None
    permission_classes = (IsAdminOrReadOnly,)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = None
    permission_classes = (IsAdminOrReadOnly,)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = None
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)

    # def perform_destroy(self, serializer):
    #     genre_slug = self.kwargs['slug']
    #     genre = get_object_or_404(Genre, slug=genre_slug)
        
