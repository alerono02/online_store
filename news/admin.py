from django.contrib import admin

from news.models import News


@admin.register(News)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'text', 'image',
                    'data_created', 'is_published', 'views_count',)
    ordering = ('data_created',)
