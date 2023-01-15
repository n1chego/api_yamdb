import csv
import os.path

from django.core.management import BaseCommand
from reviews.models import Comment
from api_yamdb import settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(os.path.join(settings.BASE_DIR,
                               'static', 'data', 'comments.csv'),
                  'r', encoding='utf-8'
                  ) as file:
            reader_csv = csv.reader(file, delimiter=',')
            next(reader_csv)
            for row in reader_csv:
                Comment.objects.update_or_create(
                    pk=int(row[0]),
                    defaults={
                        'pk': int(row[0]),
                        'review_id': int(row[1]),
                        'text': row[2],
                        'author_id': int(row[3]),
                        'pub_date': row[4]
                    }
                )
