# Generated by Django 5.1.1 on 2024-09-26 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='collections',
            field=models.ManyToManyField(blank=True, related_name='links', to='api.collection'),
        ),
    ]
