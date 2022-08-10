from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from reviews.models import Comment, Review
from .serializers import ReviewSerializer, CommentSerializer


class CommentViewSet(viewsets.ModelViewSet):
    pagination_class = LimitOffsetPagination
    # permission_classes = ...
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        return super().perform_create(serializer)

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        comments_queryset = Comment.objects.filter(review=review_id)
        return comments_queryset


class ReviewViewSet(viewsets.ModelViewSet):
    pagination_class = LimitOffsetPagination
    # permission_classes = ...
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        return super().perform_create(serializer)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review_queryset = Review.objects.filter(title=title_id)
        return review_queryset
