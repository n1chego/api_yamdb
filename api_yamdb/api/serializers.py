import datetime as dt
from django.db import IntegrityError

from rest_framework import serializers
from rest_framework.serializers import ValidationError
from rest_framework.validators import UniqueTogetherValidator
from django.contrib.auth import get_user_model
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken

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

class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)
    def validate(self, attrs):
        user = get_object_or_404(
            get_user_model(), username=attrs.get('username')
        )
        if user.confirmation_code != attrs.get('confirmation_code'):
            raise serializers.ValidationError(
                'Неверный код подтверждения'
            )
        refresh = RefreshToken.for_user(user)
        data = {'access_token': str(refresh.access_token)}
        return data


class UserSignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate(self, attrs):
        super().validate(attrs)
        if attrs.get('username') == 'me':
            raise serializers.ValidationError(
                'Неверное имя пользователя'
            )
        return attrs


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )

    def nonadmin_update(self, instance, validated_data):
        validated_data.pop('role', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


        