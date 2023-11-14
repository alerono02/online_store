from django.urls import path

from main.views import index, contacts

urlpatterns = [
    path('', index),
    path('contacts/', contacts)
]
