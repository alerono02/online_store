from django.urls import path

from orders.apps import OrdersConfig
from orders.views import OrderListView, OrderDetailView, OrderCreateView


app_name = OrdersConfig.name

urlpatterns = [
    path('', OrderListView.as_view(), name='list'),
    path('<int:pk>/', OrderDetailView.as_view(), name='detail'),
    path('create/', OrderCreateView.as_view(), name='create'),
]
