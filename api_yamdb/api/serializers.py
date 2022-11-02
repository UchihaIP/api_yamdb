from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Genre, Title
import datetime as dt

from users.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    name = serializers.StringRelatedField(
        read_only=True,
    )

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    # rating = serializers.SerializerMethodField()
    genre = GenreSerializer()
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
    )

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Title
        read_only_fields = ('id', 'description')

    def get_rating(self, obj):
        pass

    def validate_year(self, value):
        year = dt.date.today().year
        if value > year:
            raise serializers.ValidationError('Проверьте год указанного произведения.')
        return value


class RegistrySerializer(serializers.Serializer):
    email = serializers.EmailField(
        max_length=100,
        required=True,
        validators=(UniqueValidator(
            queryset=User.objects.all())
        )
    )
    username = serializers.CharField(
        max_length=100,
        required=True
    )


class JWTTokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=100,
        required=True
    )
    confirmation_code = serializers.CharField(
        max_length=30,
        required=True
    )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'role',
                  'first_name', 'last_name', 'bio')

    def validate_username(self, username):
        user = User.objects.filter(username=username).exists()
        if user:
            raise serializers.ValidationError(
                "Пользователь с данным именем уже существует."
            )
        return username
