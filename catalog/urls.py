from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.views import IndexView, ContactsView, ProductDetailView, ProductCreateView, ProductUpdateView, \
    ProductDeleteView, public_product, CategoryListView, CategoryDetailView, CategoryCreateView
from catalog.apps import MainConfig

app_name = MainConfig.name

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('view/<int:pk>/',cache_page(60)(ProductDetailView.as_view()), name='view'),
    path('edit/<int:pk>/', ProductUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name='delete'),
    path('create/', ProductCreateView.as_view(), name='create'),

    path('category/', CategoryListView.as_view(), name='category'),
    path('category/create', CategoryCreateView.as_view(), name='category_create'),
    path('category/<int:pk>/', CategoryDetailView.as_view(), name='category_products'),

    path('public_product/<int:pk>/', public_product, name='public_product')
]
