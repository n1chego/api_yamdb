from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from titles.models import Comment, User, Category, Genre, Title, Review
from .serializers import (CommentSerializer, CategorySerializer,
                          GenreSerializer, TitleSerializer,
                          ReviewSerializer)
from .permissions import AdminOrRead, OwnerOrRead, ModerOrRead


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = LimitOffsetPagination
    filterset_fields = ('category__slug', 'genre__slug', 'name', 'year')


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (OwnerOrRead, AdminOrRead, ModerOrRead)
    filter_backends = (DjangoFilterBackend,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        new_queryset = Comment.objects.filter(
            review=get_object_or_404(Review, id=review_id, title=title_id)
        )
        return new_queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, title__id=title_id, id=review_id)
        serializer.save(author=self.request.user, review=review)

    def perform_update(self, serializer):
        return super(ReviewViewSet, self).perform_update(serializer)

    def perform_destroy(self, serializer):
        return super(ReviewViewSet, self).perform_destroy(serializer)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (OwnerOrRead, AdminOrRead, ModerOrRead)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        get_object_or_404(Title, id=title_id)
        new_queryset = Review.objects.filter(title=title_id)
        return new_queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)

    def perform_update(self, serializer):
        return super(ReviewViewSet, self).perform_update(serializer)

    def perform_destroy(self, serializer):
        return super(ReviewViewSet, self).perform_destroy(serializer)
