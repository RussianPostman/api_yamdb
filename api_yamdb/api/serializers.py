from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import (Comment, Review, Genre, Category, Title,
                            GenreConnect)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('review',)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('title',)


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class TitleSerializer(serializers.ModelSerializer):

    genre = GenreSerializer(many=True)
    category = CategorySerializer(many=True)

    class Meta:
        fields = '__all__'
        model = Title

        def create(self, validated_data):
            genres = validated_data.pop('genre')
            category = validated_data.pop('category')

            categoru_from_bd, status = get_object_or_404(Category,
                                                         slug=category)
            validated_data[category] = categoru_from_bd.id
            # title = Title.objects.create(**validated_data,
            #                             category=categoru_from_bd)
            title = Title.objects.create(**validated_data)

            for genre in genres:
                current_genre, status = Genre.objects.get_or_create(
                    **genre)
                # Не забыв указать к какому котику оно относится
                GenreConnect.objects.create(
                    title=title, genre=current_genre)
            return title
