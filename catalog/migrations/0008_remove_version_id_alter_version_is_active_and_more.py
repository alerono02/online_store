# Generated by Django 4.2.7 on 2024-01-14 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_version'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='version',
            name='id',
        ),
        migrations.AlterField(
            model_name='version',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='активная версия'),
        ),
        migrations.AlterField(
            model_name='version',
            name='number_version',
            field=models.IntegerField(primary_key=True, serialize=False, verbose_name='Номер версии'),
        ),
    ]
