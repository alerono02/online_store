# Generated by Django 4.2.7 on 2024-11-02 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_alter_news_data_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='data_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания'),
        ),
    ]
