import csv
import os
from django.db import migrations
from django.conf import settings

def load_initial_user_data(apps, schema_editor):
    data_dir = os.path.join(settings.BASE_DIR, 'static', 'data')
    

    if not os.path.exists(data_dir):
        return

    User = apps.get_model('users', 'User')
    Category = apps.get_model('reviews', 'Category')
    Genre = apps.get_model('reviews', 'Genre')
    Title = apps.get_model('reviews', 'Title')
    GenreConnect = apps.get_model('reviews', 'GenreConnect')
    Review = apps.get_model('reviews', 'Review')
    Comment = apps.get_model('reviews', 'Comment')

    users_file = os.path.join(settings.BASE_DIR, 'static', 'data', 'users.csv')
    
    # Наполение пользователей
    with open(users_file, encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        _ = next(reader, None)
        users = []

        for row in reader:
            csv_user = User(
                id=row[0],
                username=row[1],
                email=row[2],
                role=row[3],
                bio=row[4],
                first_name=row[5],
                last_name=row[6]
            )
            users.append(csv_user)

    User.objects.bulk_create(users)

    # Наполнение категорий
    categories_file = os.path.join(settings.BASE_DIR, 'static', 'data', 'category.csv')

    with open(categories_file, encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        _ = next(reader, None)
        categories = []

        for row in reader:
            csv_category = Category(
                id=row[0],
                name=row[1],
                slug=row[2]
            )
            categories.append(csv_category)

    Category.objects.bulk_create(categories)
    
    # Наполнение жанров
    genres_file = os.path.join(settings.BASE_DIR, 'static', 'data', 'genre.csv')

    with open(genres_file, encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        _ = next(reader, None)
        genres = []

        for row in reader:
            csv_genre = Genre(
                id = row[0],
                name = row[1],
                slug = row[2]
            )
            
            genres.append(csv_genre)

    Genre.objects.bulk_create(genres)

    # Наполение произведений искусства
    titles_file = os.path.join(settings.BASE_DIR, 'static', 'data', 'titles.csv')

    with open(titles_file, encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        _ = next(reader, None)
        titles = []

        for row in reader:
            csv_title = Title(
                id = row[0],
                name = row[1],
                year = row[2],
                category_id = row[3]
            )

            titles.append(csv_title)
    
    Title.objects.bulk_create(titles)

    # Наполнение таблицы связки
    genre_connect_file = os.path.join(settings.BASE_DIR, 'static', 'data', 'genre_title.csv')

    with open(genre_connect_file) as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        _ = next(reader, None)
        genre_connects = []

        for row in reader:
            csv_genre = GenreConnect(
                id = row[0],
                title_id = row[1],
                genre_id = row[2]
            )
            
            genre_connects.append(csv_genre)

    GenreConnect.objects.bulk_create(genre_connects)

    # Наполнение таблицы отзывов
    review_file = os.path.join(settings.BASE_DIR, 'static', 'data', 'review.csv')

    with open(review_file, encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        _ = next(reader, None)
        reviews = []

        for row in reader:
            csv_review = Review(
                id = row[0],
                title_id = row[1],
                text = row[2],
                author_id = row[3],
                score = row[4],
                pub_date = row[5]
            )
            
            reviews.append(csv_review)

    Review.objects.bulk_create(reviews)

    # Наполнение таблицы комментариев
    comment_file = os.path.join(settings.BASE_DIR, 'static', 'data', 'comments.csv')

    with open(comment_file, encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        _ = next(reader, None)
        comments = []

        for row in reader:
            csv_comment = Comment(
                id = row[0],
                review_id = row[1],
                text = row[2],
                author_id = row[3],
                pub_date = row[4]
            )
            
            comments.append(csv_comment)

    Comment.objects.bulk_create(comments)


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_initial_user_data)
    ]
