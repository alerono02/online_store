from django.utils import timezone
from django.db import models
from django import forms

from users.models import User

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
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    description = models.TextField(verbose_name='Описание', **NULLABLE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    image = models.ImageField(upload_to='products/', verbose_name='Изображение', **NULLABLE)
    price = models.PositiveIntegerField(verbose_name='Цена')
    data_created = models.DateField(verbose_name='Дата создания', auto_now=True)
    data_changed = models.DateField(verbose_name='Дата последнего изменения', auto_now_add=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'


class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='продукт')
    title = models.CharField(max_length=150, verbose_name='Наименование')
    number_version = models.IntegerField(primary_key=True, verbose_name='Номер версии')
    is_active = models.BooleanField(verbose_name='активная версия', default=False)

    def save(self, *args, **kwargs):
        if self.is_active:  # Если эта версия должна быть активной
            versions_set = Version.objects.filter(product=self.product)  # Получаем все версии продукта
            for vers in versions_set:
                vers.is_active = False  # Делаем все версии неактивными
                vers.save()  # Сохраняем изменения
        super().save(*args, **kwargs)


def __str__(self):
    return self.title


class Meta:
    verbose_name = 'Версия продукта'
    verbose_name_plural = 'Версии продукта'
