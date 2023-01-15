from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=16)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField(
        db_index=True
    )
    category = models.ForeignKey(
        Category,
        related_name='titles',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    genre = models.ManyToManyField(Genre, through='GenreTitle')
    description = models.TextField(
        null=True,
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.title_id} {self.genre_id}'
