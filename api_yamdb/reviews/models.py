from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator


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


class Title(models.Model):
    """Произведение искусства."""

    name = models.CharField(
        max_length=100,
        verbose_name='Название произведения.'
    )
    year = models.IntegerField(
        verbose_name='Год создания.'
    )
    rating = models.SmallIntegerField(
        default=None,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10),
        ],
        verbose_name='Рейтинг',
        null=True, blank=True
    )
    description = models.TextField(
        verbose_name='Описание произведения.',
        blank=True,
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreConnect',
        related_name='genre',
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='category',
        verbose_name='Категория',
    )


class Review(models.Model):
    title = models.ForeignKey(
        to=Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    score = models.SmallIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10),
        ],
        verbose_name='Оценка',
    )
    pub_date = models.DateTimeField(
        verbose_name='Время добавления',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Ревью'
        verbose_name_plural = 'Ревью'

    def __str__(self):
        return f'{self.author.username}: {self.text}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        title = self.title
        rating = Review.objects.filter(title=title).aggregate(
            average=models.Avg('score'))
        if rating['average']:
            title.rating = int(rating['average'])
        title.save()


class Comment(models.Model):
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    review = models.ForeignKey(
        to=Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Ревью'
    )
    pub_date = models.DateTimeField(
        verbose_name='Время добавления',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'{self.author.username}: {self.text}'


class GenreConnect(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return self.genre
