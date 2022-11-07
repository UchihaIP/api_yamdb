import datetime as dt
import re

from django.db.models import Avg
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from reviews.models import Category, Genre, Title, Review, Comment, GenreTitle
from users.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class GenreCreateSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('slug',)
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()

    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
    )

    class Meta:
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category')
        model = Title
        read_only_fields = ('id', 'rating')

    def get_rating(self, obj):
        reviews_to_title = Review.objects.filter(title=obj.id).aggregate(Avg('score'))
        avg_score = reviews_to_title['score__avg']
        if avg_score is None:
            return None
        return round(avg_score)

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['category'] = CategorySerializer(instance.category).data
        response['genre'] = GenreSerializer(instance.genre, many=True).data
        return response

    def create(self, validated_data):
        genre_slugs = validated_data.pop('genre')
        title = Title.objects.create(**validated_data)
        for genre_slug in genre_slugs:
            current_genre = Genre.objects.get(slug=genre_slug.slug)
            GenreTitle.objects.create(
                genre=current_genre, title=title)
        return title

    def validate_year(self, value):
        year = dt.date.today().year
        if value > year:
            raise serializers.ValidationError('Год не должен быть больше текущего.')
        return value


class RegistrySerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=100,
        required=True
    )
    email = serializers.EmailField(
        max_length=100,
        required=True
    )

    def validate_username(self, value):
        if value == 'me':
            raise ValidationError(
                "Использовать имя 'me' в качестве username запрещено.")
        if re.search(r'^[a-zA-Z][a-zA-Z0-9-_\.]{1,20}$', value) is None:
            raise ValidationError(
                "В имени есть недопустимые символы")
        return value

    class Meta:
        fields = ('username', 'email')


class JWTTokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=100,
        required=True
    )
    confirmation_code = serializers.CharField(
        max_length=30,
        required=True
    )

    class Meta:
        fields = ('username', 'confirmation_code')


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


class UserMeChangeSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        read_only_fields = ('username', 'email', 'role')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review
        # validators = (validators.UniqueTogetherValidator(queryset=Review.objects.all(), fields=('author', 'title_id')),)
        read_only_field = ('title',)

    def validate(self, attrs):
        if attrs['score'] < 1 or attrs['score'] > 10:
            raise serializers.ValidationError('Оценка должна быть от 1 до 10!')
        return super().validate(attrs)


class CommentSerialiser(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
        read_only_field = ('review',)
