from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

User = get_user_model()


class Category(models.Model):
    """Категории произведений."""

    name = models.CharField(
        max_length=256,
        verbose_name='Название категории.'
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name='Слаг категории.'
    )


class Genre(models.Model):
    """Жанры произведений."""

    name = models.CharField(
        max_length=256,
        verbose_name='Название категории.'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Слаг жанра.'
    )


class Titles(models.Model):
    """Произведение искусства."""

    name = models.CharField(
        max_length=100,
        verbose_name='Название произведения.'
    )
    year = models.IntegerField(
        validators=[
            MaxValueValidator(2022),
        ],
        verbose_name='Год создания.'
    )
    rating = models.SmallIntegerField(
        default=None,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10),
        ],
        verbose_name='Рейтинг'
    )
    description = models.TextField(
        verbose_name='Описание произведения.',
        blank=True, null=True
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreСonnect'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='category',
        verbose_name='Категория',
    )


class RatingValue(models.Model):
    """Значения рейтинга."""

    value = models.SmallIntegerField(
        default=0
    )

    def __str__(self) -> str:
        return self.value

    class Meta:
        verbose_name = 'Значение рейтинга'


class Rating(models.Model):
    """Рейтинг."""

    rating = models.ForeignKey(
        RatingValue,
        on_delete=models.CASCADE,
        verbose_name='Рейтинг'
    )
    title = models.ForeignKey(
        Titles,
        on_delete=models.CASCADE,
        verbose_name='Произведение искусства'
    )

    def __str__(self) -> str:
        return f'{self.rating} - {self.title}'

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'
