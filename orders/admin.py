from django.contrib import admin

from orders.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'get_product_names', 'status', 'phone',
                    'address', 'delivery_date', 'total_cost', 'date_created',)
    ordering = ('date_created',)

    def get_product_names(self, obj):
        return ', '.join([product.name for product in obj.products.all()])

    get_product_names.short_description = 'Товары'
