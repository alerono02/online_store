from django.shortcuts import render
from catalog.models import Product
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DetailView, DeleteView


def index(request):
    product_list = Product.objects.all()
    context = {
        'object_list': product_list,
        'title': 'Главная',
        'mediapath': '/media/'
    }
    return render(request, 'catalog/index.html', context)


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        text = request.POST.get('message')
        print(f'{name} ({phone}): {text}')

    context = {
        'title': 'Главная'
    }

    return render(request, 'catalog/contacts.html', context)


class ProductDetailView(DetailView):
    """Контроллер просмотра отдельного продукта"""
    model = Product
