from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters, permissions, viewsets
from rest_framework.pagination import LimitOffsetPagination

from titles.models import Comment, User, Category, Genre, Title, Review
from .permissions import AdminOrRead
from .serializers import (CommentSerializer, CategorySerializer,
                          GenreSerializer, TitleWriteSerializer,
                          ReviewSerializer, TitleViewSerializer)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleWriteSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (AdminOrRead,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre', 'name', 'year')

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return TitleWriteSerializer
        return TitleViewSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination
    # permission_classes = (OwnerOrRead, AdminOrRead, ModerOrRead)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        new_queryset = Comment.objects.filter(review__title=title_id, review=review_id)
        return new_queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, title__id=title_id, id=review_id)
        serializer.save(author=self.request.user, review=review)

    def perform_update(self, serializer):
        # Тут или проверка на авторство или ничего, если описан permission_class
        return super(ReviewViewSet, self).perform_update(serializer)

    def perform_destroy(self, serializer):
        # Тут или проверка на авторство или ничего, если описан permission_class
        return super(ReviewViewSet, self).perform_destroy(serializer)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    permission_classes = (AdminOrRead,)
    search_fields = ('name',)
    lookup_field = 'slug'


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    permission_classes = (AdminOrRead,)
    search_fields = ('name',)
    lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination
    # permission_classes = (OwnerOrRead, AdminOrRead, ModerOrRead)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        new_queryset = Review.objects.filter(title=title_id)
        return new_queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)

    def perform_update(self, serializer):
        # Тут или проверка на авторство или ничего, если описан permission_class
        return super(ReviewViewSet, self).perform_update(serializer)

    def perform_destroy(self, serializer):
        # Тут или проверка на авторство или ничего, если описан permission_class
        return super(ReviewViewSet, self).perform_destroy(serializer)
