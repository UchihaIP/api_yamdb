from rest_framework import serializers
from reviews.models import Category, Genre, Title, GenreTitle
import datetime as dt
from django.db.models import Avg


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):

    rating = serializers.SerializerMethodField()
    # rating = serializers.IntegerField(default=0)
    genre = serializers.SlugRelatedField(
        queryset = Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    category = serializers.SlugRelatedField(
        queryset = Category.objects.all(),
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
            return 0
        return float('{:.1f}'.format(avg_score))


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
