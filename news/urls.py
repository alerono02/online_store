from django.urls import path
from news.views import NewsCreateView, NewsListView, NewsDetailView, NewsUpdateView, NewsDeleteView
from news.apps import NewsConfig

app_name = NewsConfig.name

urlpatterns = [
    path('',NewsListView.as_view(), name='list'),
    path('create/', NewsCreateView.as_view(), name='create'),
    path('view/<int:pk>/', NewsDetailView.as_view(), name='view'),
    path('edit/<int:pk>/', NewsUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>/', NewsDeleteView.as_view(), name='delete'),
]


