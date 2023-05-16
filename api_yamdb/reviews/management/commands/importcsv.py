import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from reviews.models import Category


class Command(BaseCommand):
    help = 'Выполнить импорт данных из csv файла'

    def handle(self, *args, **kwargs):
        path = settings.STATICFILES_DIRS[0] / 'data' / 'category.csv'
        with open(path, encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                obj, created = Category.objects.get_or_create(
                    id=row[0],
                    name=row[1],
                    slug=row[2],
                )
        print('Данные категорий загружены в БД')
