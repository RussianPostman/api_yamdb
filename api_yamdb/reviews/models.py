from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Review(models.Model):
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        to=User,
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


class Comment(models.Model):
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        to=User,
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
