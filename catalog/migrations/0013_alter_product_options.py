# Generated by Django 4.2.7 on 2024-02-03 18:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0012_alter_product_options_remove_product_is_active_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'permissions': [('set_published', 'Can publish post')], 'verbose_name': 'продукт', 'verbose_name_plural': 'продукты'},
        ),
    ]
