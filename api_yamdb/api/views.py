from reviews.models import Category, Genre, Title

from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework import mixins
from .serializers import (CategorySerializer, GenreSerializer, TitleSerializer)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from .filters import TitleFilter

class CreateListDestroyViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, 
    mixins.DestroyModelMixin ,viewsets.GenericViewSet):
    pass


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (AllowAny,)  #IsAdminOrReadOnly


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    permission_classes = (AllowAny,)  #IsAdminOrReadOnly
    lookup_field = 'slug'


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    permission_classes = (AllowAny,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
