from django.contrib import admin
from catalog.models import Category, Product, Version


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    ordering = ('id',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'name', 'price', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'description')
    ordering = ('id',)


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ('product', 'title', 'number_version', 'is_active')
    list_filter = ('product',)
