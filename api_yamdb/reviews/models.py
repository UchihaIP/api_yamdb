from django.db import models
from django.db.models import TextField

from users.models import User


class Category(models.Model):
    """Класс категорий"""
    name = models.CharField(max_length=256,
                            verbose_name='Название категории')
    slug = models.SlugField(max_length=50,
                            unique=True)


class Genre(models.Model):
    """Класс жанров"""
    name = models.CharField(max_length=256,
                            verbose_name='Название жанра')
    slug = models.SlugField(max_length=50,
                            unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    """Класс произведений"""
    name = models.CharField(max_length=256,
                            verbose_name='Название произведения')
    year = models.IntegerField(db_index=True)
    description = models.TextField(blank=True,
                                   null=True)
    genre = models.ManyToManyField(Genre,
                                   through='GenreTitle')
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles'
    )

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """Связующая модель"""
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)


class Review(models.Model):
    """Класс отзывов."""
    text = models.TextField(verbose_name='Текст отзыва')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='reviews')
    score = models.IntegerField()
    pub_date = models.DateTimeField('Дата публикации',
                                    auto_now_add=True)
    title = models.ForeignKey(Title,
                              on_delete=models.CASCADE,
                              related_name='reviews')

    class Meta:
        constraints = [models.UniqueConstraint(fields=['title', 'author'],
                                               name='unique_user_make_review')]

    def __str__(self) -> TextField:
        return self.text[20:]


class Comment(models.Model):
    """Класс комментариев."""
    text = models.TextField(verbose_name='Текст комментария')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='comments')
    pub_date = models.DateTimeField('Дата публикации',
                                    auto_now_add=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE,
                               related_name='comments')

    def __str__(self) -> TextField:
        return self.text[20:]
