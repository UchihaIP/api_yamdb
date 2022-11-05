import time

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from reviews.models import Category, Genre, Title, Review
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, mixins
from rest_framework.filters import SearchFilter
from rest_framework_simplejwt.tokens import RefreshToken

from api_yamdb.settings import CONTACT_EMAIL
from users.models import User
from .permissions import IsAdmin, IsAdminOrReadOnly
from .serializers import (
    CategorySerializer, GenreSerializer, TitleSerializer, RegistrySerializer,
    JWTTokenSerializer, UserSerializer, ReviewSerialiser, CommentSerialiser)


class CreateListDestroyViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, 
    mixins.DestroyModelMixin ,viewsets.GenericViewSet):
    pass


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = None
    permission_classes = (IsAdminOrReadOnly,)


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = None
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = None
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class RegistryView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        serializer = RegistrySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get("email")
        username = serializer.validated_data.get("username")
        if serializer.is_valid():
            confirmation_code = str(time.time())[-5:]
            user = User.objects.get(
                username=username
            )
            if user:
                return Response('Такой пользователь уже существует',
                                status=status.HTTP_403_FORBIDDEN)

            User.objects.create_user(username=username,
                                     email=email)
            User.objects.get(username).update(confirmation_code=
                                              confirmation_code)
            send_mail(
                subject="Ваш код для доступа",
                message=confirmation_code,
                from_email=CONTACT_EMAIL,
                recipient_list=[email]
            )
            return Response(serializer.data,
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JWTTokenView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        serializer = JWTTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(
            username=serializer.validated_data['username']
        )
        if not user:
            return Response(
                'Пользователь не найден!',
                status=status.HTTP_404_NOT_FOUND
            )
        if serializer.validated_data.get(
                'confirmation_code') == user.confirmation_code:
            token = RefreshToken.for_user(user).access_token
            return Response(
                {
                    'token': str(token)
                },
                status=status.HTTP_201_CREATED)
        return Response(
            'Access_denied',
            status=status.HTTP_400_BAD_REQUEST
        )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (SearchFilter,)
    search_fields = ("username",)


class UserProfileViewSet(APIView):
    # !create get and patch methods
    def get(self, request):
        if request.user.is_authenticated:
            serializer = UserSerializer(request.user)
            return Response(serializer.data)
        return Response(
            'У нас нет доступа к ресурсу',
            status=status.HTTP_401_UNAUTHORIZED
        )

    def patch(self, request):
        if request.user.is_authenticated:
            if request.user.is_admin:
                serializer = UserSerializer(
                    request.user,
                    data=request.data,
                    partial=True
                )
            else:
                serializer = UserSerializer(
                    request.user,
                    data=request.data,
                    partial=True
                )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(
            'У нас нет доступа к ресурсу',
            status=status.HTTP_401_UNAUTHORIZED
        )


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerialiser
    permission_classes = (AllowAny,)
    
    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        return title.reviews

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        serializer.save(title=title, author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerialiser
    permission_classes = (AllowAny,)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs['review_id'])
        return review.comments

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs['review_id'])
        serializer.save(review=review, author=self.request.user)
