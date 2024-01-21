from django.contrib.auth.models import AbstractUser
from django.db import models
from django_countries.fields import CountryField


NULLABLE = {'null': True, 'blank': True}

# Create your models here.
class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='Email')
    phone = models.CharField(max_length=35, verbose_name='номер телефона', **NULLABLE)
    country = CountryField(blank_label="(выберите страну)", **NULLABLE)
    avatar = models.ImageField(upload_to='users', verbose_name='аватар', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
