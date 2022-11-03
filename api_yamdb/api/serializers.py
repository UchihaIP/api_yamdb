from rest_framework import serializers
from reviews.models import Category, Genre, Title, GenreTitle
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

    genre = GenreSerializer(many=True)
    category = serializers.SlugRelatedField(
        queryset = Category.objects.all(),
        slug_field='slug',
    )
    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Title
        read_only_fields = ('id', 'description')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['category'] = CategorySerializer(instance.category).data
        return response

    def create(self, validated_data):
        # Уберем список жанров из словаря validated_data и сохраним его
        genre = validated_data.pop('genre')

        # Создадим новое произведение пока без жанров, данных нам достаточно
        title = Title.objects.create(**validated_data)

        # Для каждого жанра из списка жанров
        for singl_genre in genre:
            # Создадим новую запись или получим существующий экземпляр из БД
            current_genre, status = Genre.objects.get_or_create(
                **singl_genre)
            # Поместим ссылку на каждый жанр во вспомогательную таблицу
            # Не забыв указать к какому произведению он относится
            GenreTitle.objects.create(
                genre=current_genre, title=title)
        return title 

    def get_rating(self, obj):
        pass

    def validate_year(self, value):
        year = dt.date.today().year
        if value > year:
            raise serializers.ValidationError('Проверьте год указанного произведения.')
        return value 
