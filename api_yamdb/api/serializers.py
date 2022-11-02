from rest_framework import serializers
from reviews.models import Category, Genre, Title
import datetime as dt


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    # rating = serializers.SerializerMethodField()
    genre = GenreSerializer()
    category = serializers.SlugRelatedField(
        queryset = Category.objects.all(),
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
            raise serializers.ValidationError('Проверье год указанного произведения.')
        return value 
