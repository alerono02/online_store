# Generated by Django 4.2.7 on 2023-12-12 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_rename_view_count_news_views_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='Превью'),
        ),
    ]