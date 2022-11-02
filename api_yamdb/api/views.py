from rest_framework.response import Response
from rest_framework.views import APIView

from reviews.models import Category, Genre, Title

from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from .permissions import IsAdmin, IsAdminOrReadOnly, IsAdminModeratirAuthor
from .serializers import (CategorySerializer,
                          GenreSerializer,
                          TitleSerializer,
                          RegistrySerializer,
                          JWTTokenSerializer, UserSerializer)


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


class RegistryView(APIView):
    def post(self, request):
        serializer = RegistrySerializer(data=request.data)
        serializer.is_valid()
        email = serializer.validated_data.get("email")
        username = serializer.validated_data.get("username")
        if serializer.is_valid():
            # confirmation_code = func_for_generatecode()
            user, _ = User.objects.get_or_create(
                username=username,
                email=email
            )
            # user.confirmation_code = confirmation_code
            # user.save()
            # mail_confirmation_code()
            return Response(serializer.validated_data, status=200)


class JWTTokenView(APIView):
    def post(self, request):
        serializer = JWTTokenSerializer(data=request.data)
        serializer.is_valid()
        confirmation_code = serializer.validated_data.get("confirmation_code")
        username = serializer.validated_data.get("username")
        user = get_object_or_404(
            User,
            username
        )
        if user.confirmation_code != confirmation_code:
            return Response("Access denied", status=400)

        return Response({
            "access_token": str(RefreshToken.for_user(user))
        })


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    search_fields = ("username",)
