# Generated by Django 4.2.7 on 2023-12-10 16:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_news_slug_news_view_count_alter_news_is_published'),
    ]

    operations = [
        migrations.RenameField(
            model_name='news',
            old_name='view_count',
            new_name='views_count',
        ),
    ]
