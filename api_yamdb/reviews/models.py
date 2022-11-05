from django.db import models
from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    description = models.TextField(blank=True)
    genre = models.ManyToManyField(Genre, through='GenreTitle')
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles'
    )

    def __str__(self):
        return self.name

class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)


class Review(models.Model):
    """Класс отзывов."""
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    score = models.IntegerField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name='reviews')

    class Meta:
        constraints = [models.UniqueConstraint(fields=['author', 'title'], name='unuque_user_make_review')]

    def __str__(self) -> str:
        return self.text


class Comment(models.Model):
    """Класс комментариев."""
    text = models.TextField()
    author = models. ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')

    def __str__(self) -> str:
        return self.text
