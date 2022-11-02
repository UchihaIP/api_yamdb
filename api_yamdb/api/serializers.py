from rest_framework import serializers, validators
from reviews.models import Category, Genre, Title, Review, Comment
import datetime as dt


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
    genre = GenreSerializer(many=True)
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
            raise serializers.ValidationError('Проверьте год указанного произведения.')
        return value

    #def create(self, validated_data):
        #genre = validated_data.pop('genre')
        #title = Title.objects.create(**validated_data)
        #for i in genre:
            #current_genre, status = Genre.objects.get_or_create(**i)



class ReviewSerialiser(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review
        validators = (validators.UniqueTogetherValidator(queryset=Review.objects.all(), fields=('author', 'title')))
        read_only_field = ('title',)

    def validate(self, attrs):
        if attrs['score'] < 1 or attrs['score'] > 10:
            raise serializers.ValidationError('Оценка должна быть от 1 до 10!')
        return super().validate(attrs)


class CommentSerialiser(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model =Comment
        read_only_field = ('review',)
