import csv
from django.core.management.base import BaseCommand
from django.conf import settings
from reviews.models import Title, Category, Genre, Review, Comment, GenreTitle
from users.models import User


class Command(BaseCommand):
    help = 'Load csv files to reviews models.'

    def handle(self, *args, **kwargs):

        with open(f'{settings.BASE_DIR}/static/data/category.csv', 'r'
                  ) as csvfile:
            Category.objects.all().delete()
            reader = csv.DictReader(csvfile)
            for row in reader:
                Category.objects.create(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug']
                )
            csvfile.close()

        with open(f'{settings.BASE_DIR}/static/data/genre.csv'
                  ) as csvfile:
            Genre.objects.all().delete()
            reader = csv.DictReader(csvfile)
            for row in reader:
                Genre.objects.create(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug'],
                )

        with open(f'{settings.BASE_DIR}/static/data/titles.csv'
                  ) as csvfile:
            reader = csv.DictReader(csvfile)
            Title.objects.all().delete()
            for row in reader:
                Title.objects.create(
                    id=row['id'],
                    name=row['name'],
                    year=row['year'],
                    category=Category.objects.get(id=row['category']),
                )

        with open(f'{settings.BASE_DIR}/static/data/genre_title.csv'
                  ) as csvfile:
            reader = csv.DictReader(csvfile)
            GenreTitle.objects.all().delete()
            for row in reader:
                GenreTitle.objects.create(
                    id=row['id'],
                    title_id=row['title_id'],
                    genre_id=row['genre_id'],
                )

        with open(f'{settings.BASE_DIR}/static/data/review.csv'
                  ) as csvfile:
            reader = csv.DictReader(csvfile)
            Review.objects.all().delete()
            for row in reader:
                Review.objects.create(
                    id=row['id'],
                    title_id=row['title_id'],
                    text=row['text'],
                    author=User.objects.get(id=row['author']),
                    score=row['score'],
                    pub_date=row['pub_date'],
                )

        with open(f'{settings.BASE_DIR}/static/data/comments.csv'
                  ) as csvfile:
            reader = csv.DictReader(csvfile)
            Comment.objects.all().delete()
            for row in reader:
                Comment.objects.create(
                    id=row['id'],
                    review_id=row['review_id'],
                    text=row['text'],
                    author=User.objects.get(id=row['author']),
                    pub_date=row['pub_date'],
                )

        return 'Распаковка csv для моделей reviews прошла успешно!'
