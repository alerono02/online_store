from django.utils import timezone
from django.db import models
from django import forms
from django.utils.translation import gettext_lazy as _


from users.models import User
from catalog.models import Product


class Order(models.Model):
    STATUS = (
        (1, 'Создан'),
        (2, 'В сборке'),
        (3, 'В доставке'),
        (4, 'Завершен'),
        (0, 'Отменен'),
    )

    user = models.ForeignKey(
        User, related_name='Пользователь', on_delete=models.CASCADE)
    products = models.ManyToManyField(
        Product, related_name='Товары', through='OrdersProducts')
    phone = models.CharField(
        max_length=35, verbose_name='Номер телефона')
    status = models.IntegerField(
        choices=STATUS, verbose_name='Статус', default=1)
    date_created = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата создания')
    delivery_date = models.DateTimeField(verbose_name='Дата доставки')
    total_cost = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Общая стоимость', null=True, blank=True)
    address = models.CharField(max_length=150, verbose_name='Адрес')

    def __str__(self):
        return f'Order №{self.id} by {self.address}'

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'


class OrdersProducts(models.Model):
    order = models.ForeignKey(
        Order, related_name='Заказы', on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name='Продукты', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='Количество')
