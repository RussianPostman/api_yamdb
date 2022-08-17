from django.contrib import admin

from .models import User
from reviews.models import Comment, Review, Genre, Category, Title


admin.site.register(User)
admin.site.register(Comment)
admin.site.register(Review)
admin.site.register(Genre)
admin.site.register(Category)
admin.site.register(Title)
