import csv
import os
from api_yamdb import settings
from django.core.management.base import BaseCommand
from titles.models import Genre


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(
                os.path.join(
                    settings.BASE_DIR,
                    'static', 'data', 'genre.csv'
                ),
                'r', encoding='utf-8'
        ) as f:
            csv_reader = csv.reader(f, delimiter=',')
            next(csv_reader)
            for row in csv_reader:
                Genre.objects.update_or_create(
                    id=int(row[0]),
                    defaults={
                        'id': int(row[0]),
                        'name': row[1],
                        'slug': row[2],
                    }
                )
