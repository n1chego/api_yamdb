from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User
from titles.models import Title


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        related_name='reviews',
        on_delete=models.CASCADE
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        related_name='reviews',
        on_delete=models.CASCADE
    )
    score = models.IntegerField(
        validators=[MaxValueValidator(10), MinValueValidator(1)]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            )
        ]
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:10]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        related_name='comments',
        on_delete=models.CASCADE
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        related_name='comments',
        on_delete=models.CASCADE
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:10]
