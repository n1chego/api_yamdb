import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from reviews.models import Title


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(
            os.path.join(
                settings.BASE_DIR,
                'static', 'data', 'titles.csv'
            ),
            'r', encoding='utf-8'
        ) as file:
            csv_reader = csv.reader(file, delimiter=',')
            next(csv_reader)
            for row in csv_reader:
                Title.objects.update_or_create(
                    id=int(row[0]),
                    defaults={
                        'id': int(row[0]),
                        'name': row[1],
                        'year': row[2],
                        'category_id': int(row[3])
                    }
                )
