from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from rest_framework import mixins
# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .filters import TitleFilter

from reviews.models import Comment, Review, Genre, Category, Title
from .serializers import (ReviewSerializer,
                          CommentSerializer,
                          GenreSerializer,
                          CategorySerializer,
                          TitleSerializer,
                          TitleCreateSerializer)


class CreateListDestroyViewSet(mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet,):
    pass


class CommentViewSet(viewsets.ModelViewSet):
    pagination_class = LimitOffsetPagination
    # permission_classes = ...
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        serializer.save(author=self.request.user, review_id=review_id)

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        comments_queryset = Comment.objects.filter(review=review_id)
        return comments_queryset


class ReviewViewSet(viewsets.ModelViewSet):
    pagination_class = LimitOffsetPagination
    # permission_classes = ...
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        serializer.save(author=self.request.user, title_id=title_id)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review_queryset = Review.objects.filter(title=title_id)
        return review_queryset


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    # permission_classes =
    filter_backends = (filters.SearchFilter,)
    # filterset_fields = ('name',)
    search_fields = ('name',)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):

    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_class = filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH',):
            return TitleCreateSerializer
        return TitleSerializer
