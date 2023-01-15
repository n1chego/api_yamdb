import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from titles.models import GenreTitle


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(
                os.path.join(
                    settings.BASE_DIR,
                    'static', 'data', 'genre_title.csv'
                ),
                'r', encoding='utf-8'
        ) as f:
            csv_reader = csv.reader(f, delimiter=',')
            next(csv_reader)
            for row in csv_reader:
                GenreTitle.objects.update_or_create(
                    id=int(row[0]),
                    defaults={
                        'id': int(row[0]),
                        'title_id': int(row[1]),
                        'genre_id': int(row[2]),
                    }
                )
