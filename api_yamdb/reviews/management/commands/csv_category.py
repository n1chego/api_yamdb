import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from titles.models import Category


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(
                os.path.join(
                    settings.BASE_DIR,
                    'static', 'data', 'category.csv'
                ),
                'r', encoding='utf-8'
        ) as file:
            csv_reader = csv.reader(file, delimiter=',')
            next(csv_reader)
            for row in csv_reader:
                Category.objects.update_or_create(
                    id=int(row[0]),
                    defaults={
                        'id': int(row[0]),
                        'name': row[1],
                        'slug': row[2],
                    }
                )
