# Generated by Django 3.2 on 2023-01-10 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('titles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='title',
            name='description',
            field=models.TextField(max_length=200, null=True),
        ),
    ]