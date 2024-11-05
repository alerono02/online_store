from django.core.management import BaseCommand
from config.settings import BASE_DIR
from catalog.models import Category, Product
import json


class Command(BaseCommand):

    def handle(self, *args, **options):

        Product.objects.all().delete()
        Category.objects.all().delete()

        try:
            with open(BASE_DIR / 'catalog/fixtures/categories.json', 'r', encoding='utf-8') as file:
                category_data = json.load(file)
                for item in category_data:
                    Category.objects.create(
                        pk=item['pk'],
                        name=item['fields']['name'],
                        description=item['fields']['description']
                    )
            with open(BASE_DIR / 'catalog/fixtures/products.json', 'r', encoding='utf-8') as file:
                product_data = json.load(file)
                for item in product_data:
                    category_pk = item['fields']['category']
                    category = Category.objects.get(pk=category_pk)
                    Product.objects.create(
                        pk=item['pk'],
                        name=item['fields']['name'],
                        description=item['fields']['description'],
                        image=item['fields']['image'],
                        category=category,
                        price=item['fields']['price'],
                        data_created=item['fields']['data_created'],
                        data_changed=item['fields']['data_changed']
                    )

        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f'Ошибка при импорте данных: {e}'))

        else:
            self.stdout.write(self.style.SUCCESS(
                'Данные успешно добавлены в базу данных'))
