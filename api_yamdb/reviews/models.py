from tabnanny import verbose
from django.db import models
from django.conf import settings


class Title(models.Model):
    ...


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
        rating = Review.objects.filter(title=title).aggregate(average=models.Avg('score'))
        title.rating = rating['average']
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
