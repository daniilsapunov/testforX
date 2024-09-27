from django.db import migrations
from django.contrib.auth.models import User
from api.models import Link
import random

def create_test_data(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Link = apps.get_model('api', 'Link')

    # Создаем тестовых пользователей
    users = [User(username=f'user{i}', password='password') for i in range(1, 21)]
    User.objects.bulk_create(users)

    # Создаем тестовые ссылки
    for user in users:
        for _ in range(random.randint(0, 15)):  # Каждый пользователь может иметь от 0 до 15 ссылок
            Link.objects.create(
                user=user,
                title=f'Test Link {random.randint(1, 100)}',
                url=f'http://example{random.randint(1, 10000000)}.com',
                image='http://example.com/image.jpg',
                link_type=random.choice(['website', 'book', 'article', 'music', 'video'])
            )

class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),  # Убедитесь, что это зависит от вашей первой миграции
    ]

    operations = [
        migrations.RunPython(create_test_data),
    ]