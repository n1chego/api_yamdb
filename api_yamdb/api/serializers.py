import datetime as dt
from django.db import IntegrityError

from rest_framework import serializers
from rest_framework.serializers import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from titles.models import Comment, User, Category, Genre, Title, Review


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()

    def validate(self, data):
        current_year = dt.datetime.today().year
        if not (data['year'] <= current_year):
            raise ValidationError('Год не подходит')
        return data

    class Meta:
        fields = '__all__'
        model = Title

    def get_rating(self, obj):
        rating = 0
        reviews = Review.objects.filter(title=obj)
        if reviews:
            for review in reviews:
                rating += review.score
            return rating // reviews.count()
        return rating


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('review',)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Genre


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault(),
        slug_field='username'
    )
    title = serializers.HiddenField(default=None)

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('title',)
        validators = [UniqueTogetherValidator(
            queryset=Review.objects.all(),
            fields=('title', 'author')
        )]

    def create(self, validated_data):
        try:
            review = Review.objects.create(**validated_data)
        except IntegrityError:
            raise serializers.ValidationError(
                {'error': 'Нельзя оставлять два ревью на одно произведение.'})
        return review
