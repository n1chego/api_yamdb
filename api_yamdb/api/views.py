from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from rest_framework import filters, permissions, viewsets

from titles.models import Comment, User, Category, Genre, Title, Review
from .serializers import (CommentSerializer, CategorySerializer,
                          GenreSerializer, TitleSerializer,
                          ReviewSerializer)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
