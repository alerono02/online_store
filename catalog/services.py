from django.core.cache import cache

from catalog.models import Category
from config.settings import CACHE_ENABLED


def category_list_cache():
    if CACHE_ENABLED:
        # Проверяем включенность кеша
        key = f'category_list'  # Создаем ключ для хранения
        category_list = cache.get(key)  # Пытаемся получить данные
        if category_list is None:
            # Если данные не были получены из кеша, то выбираем из БД и записываем в кеш
            students_list = Category.objects.all()
            cache.set(key, students_list)
    else:
        # Если кеш не был подключен, то просто обращаемся к БД
        category_list = Category.objects.all()
    # Возвращаем результат
    return category_list
