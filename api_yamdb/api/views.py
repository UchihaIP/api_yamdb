from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action, api_view
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .filters import TitleFilter
from .permissions import IsAdmin, IsAdminOrReadOnly, IsAdminModeratorAuthor
from .serializers import (
    CategorySerializer, GenreSerializer, TitleSerializer, RegistrySerializer,
    JWTTokenSerializer, UserSerializer, UserMeChangeSerializer,
    ReviewSerializer, CommentSerialiser)
from api_yamdb import settings
from reviews.models import Category, Genre, Title, Review
from api_yamdb.settings import CONTACT_EMAIL
from reviews.models import Category, Genre, Title, Review, Comment
from users.models import User


class CreateListDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass


class TitleViewSet(viewsets.ModelViewSet):
    queryset = (Title.objects.all()
                .select_related('category')
                .prefetch_related('genre')
                .annotate(
        rating=Avg('reviews__score')
    )
                .order_by('name'))
    serializer_class = TitleSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


@api_view(["POST"])
def RegistryView(request):
    serializer = RegistrySerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data.get("email")
    username = serializer.validated_data.get("username")
    try:
        user, _ = User.objects.get_or_create(username=username,
                                             email=email)
        confirmation_code = default_token_generator.make_token(user)
        _send_email(email, confirmation_code)
        user.confirmation_code = confirmation_code
        user.save()
    except IntegrityError:
        return Response('Такой пользователь уже существует, \n'
                        'Код отправлен существующему пользователю',
                        status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.validated_data, status=status.HTTP_200_OK)


@api_view(["POST"])
def JWTTokenView(request):
    serializer = JWTTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    user = get_object_or_404(User, username=username)
    confirmation_code = serializer.validated_data.get('confirmation_code')
    if confirmation_code == user.confirmation_code:
        token = str(AccessToken.for_user(user))
        return Response({'token': token},
                        status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(
        detail=False,
        methods=['GET', 'PATCH'],
        permission_classes=[IsAuthenticated, ],
        url_path='me',
        url_name='my_profile'
    )
    def get_or_change_profile_info(self, request):
        if request.method == "GET":
            serializer = UserMeChangeSerializer(request.user,
                                                data=request.data)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data,
                            status=status.HTTP_200_OK)
        if request.method == "PATCH":
            serializer = UserMeChangeSerializer(request.user,
                                                data=request.data,
                                                partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_200_OK)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminModeratorAuthor,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        return Review.objects.select_related('author').filter(title=title)

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        serializer.save(title=title, author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerialiser

    permission_classes = (IsAdminModeratorAuthor,)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs['review_id'])
        return Comment.objects.select_related('author').filter(review=review)

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs['review_id'])
        serializer.save(review=review, author=self.request.user)


def _send_email(email, confirmation_code):
    send_mail(
        subject="Ваш код для доступа",
        message=confirmation_code,
        from_email=settings.CONTACT_EMAIL,
        recipient_list=[email]
    )
