from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from catalog.views import index, contacts

urlpatterns = [
    path('', index),
    path('contacts/', contacts),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
