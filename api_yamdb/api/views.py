from rest_framework import viewsets

class CommentViewSet(viewsets.ModelViewSet):
    # pagination_class = ...
    # permission_classes = ...
    # serializer_class = ...
    def perform_create(self, serializer):
        return super().perform_create(serializer)

    def get_queryset(self):
        return super().get_queryset()


class ReviewViewSet(viewsets.ModelViewSet):
    # pagination_class = ...
    # permission_classes = ...
    # serializer_class = ...
    def perform_create(self, serializer):
        return super().perform_create(serializer)

    def get_queryset(self):
        return super().get_queryset()
