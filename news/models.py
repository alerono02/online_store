from django.db import models


class News(models.Model):
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    slug = models.CharField(
        max_length=150, verbose_name='slug',  null=True, blank=True)
    text = models.TextField(verbose_name='Содержимое')
    image = models.ImageField(verbose_name='Превью', null=True, blank=True)
    data_created = models.DateTimeField(
        verbose_name='Дата создания', auto_now_add=True)
    is_published = models.BooleanField(
        verbose_name='Опубликовано', default=True)
    views_count = models.IntegerField(default=0, verbose_name='Просмотры')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'новость'
        verbose_name_plural = 'новости'
