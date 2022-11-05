from reviews.models import Category, Genre, Title, Review

from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny

from .serializers import (CategorySerializer, GenreSerializer, TitleSerializer, ReviewSerialiser, CommentSerialiser)

from users.models import User


class CreateListDestroyViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, 
    mixins.DestroyModelMixin ,viewsets.GenericViewSet):
    pass
    

class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = None
    permission_classes = (AllowAny,)  #IsAdminOrReadOnly

class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = None
    permission_classes = (AllowAny,)  #IsAdminOrReadOnly
    lookup_field = 'slug'


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = None
    permission_classes = (AllowAny,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerialiser
    permission_classes = (AllowAny,)
    
    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        return title.reviews

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        serializer.save(title=title, author=User.objects.get(pk=1))


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerialiser
    permission_classes = (AllowAny,)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs['review_id'])
        return review.comments

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs['review_id'])
        serializer.save(review=review, author=User.objects.get(pk=1))
