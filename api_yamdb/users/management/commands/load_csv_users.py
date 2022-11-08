import csv
import os
from django.conf import settings
from django.core.management.base import BaseCommand

from users.models import User

dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
PATH_TO_FILE = os.path.abspath(f'{parent_dir_path}/static/data/')

Model_vs_file = {
    User: "users.csv",
}


class Command(BaseCommand):
    help = 'Load csv files to users models.'

    def handle(self, *args, **kwargs):
        with open(f'{settings.BASE_DIR}/static/data/users.csv',
                  'r') as csvfile:
            reader = csv.DictReader(csvfile)
            User.objects.all().delete()
            for row in reader:
                User.objects.create(
                    id=row['id'],
                    username=row['username'],
                    email=row['email'],
                    role=row['role'],
                    bio=row['bio'],
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                )
            return 'Распаковка csv файла модели User прошла успешно!'
