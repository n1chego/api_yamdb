from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters, viewsets
from rest_framework.pagination import PageNumberPagination

from .filters import TitleFilter
from .mixins import MixinViewSet
from .permissions import AdminOrRead, OwnerOrRead
from .serializers import (CommentSerializer, CategorySerializer,
                          GenreSerializer, TitleWriteSerializer,
                          ReviewSerializer, TitleViewSerializer)
from reviews.models import Comment, Review
from titles.models import Category, Genre, Title


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleWriteSerializer
    pagination_class = PageNumberPagination
    permission_classes = (AdminOrRead,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return TitleWriteSerializer
        return TitleViewSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination
    permission_classes = (
        OwnerOrRead,
    )

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        new_queryset = Comment.objects.filter(
            review__title=title_id,
            review=review_id
        )
        return new_queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, title__id=title_id, id=review_id)
        serializer.save(author=self.request.user, review=review)

    def perform_update(self, serializer):
        return super(CommentViewSet, self).perform_update(serializer)

    def perform_destroy(self, serializer):
        return super(CommentViewSet, self).perform_destroy(serializer)


class GenreViewSet(MixinViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    permission_classes = (AdminOrRead,)
    search_fields = ('name',)
    lookup_field = 'slug'


class CategoryViewSet(MixinViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    permission_classes = (AdminOrRead,)
    search_fields = ('name',)
    lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination
    permission_classes = (
        OwnerOrRead,
    )

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
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
