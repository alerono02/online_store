from django.utils import timezone
from django.db import models

NULLABLE = {'null': True, 'blank': True}


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='Категория')
    description = models.CharField(max_length=500, verbose_name='Описание', **NULLABLE)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Наименование')
    description = models.CharField(max_length=500, verbose_name='Описание', **NULLABLE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    image = models.ImageField(upload_to='products/', verbose_name='Изображение', **NULLABLE)
    price = models.IntegerField(verbose_name='Цена')
    data_created = models.DateField(verbose_name='Дата создания', auto_now=True)
    data_changed = models.DateField(verbose_name='Дата последнего изменения', auto_now_add=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
