from django.urls import path

from catalog.views import index, contacts, ProductDetailView
from catalog.apps import MainConfig

app_name = MainConfig.name

urlpatterns = [
    path('', index, name='index'),
    path('contacts/', contacts, name='contacts'),
    path('view/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
]
