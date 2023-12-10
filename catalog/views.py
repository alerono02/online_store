from django.shortcuts import render
from catalog.models import Product
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DetailView, DeleteView


class IndexView(TemplateView):
    """Контроллер просмотра домашней страницы"""
    template_name = 'catalog/index.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['object_list'] = Product.objects.all()
        context_data['title'] = 'Главная'
        return context_data


class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Контакты'
        return context_data

    def post(self, request):
        if request.method == 'POST':
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            text = request.POST.get('message')
        print(f'You have new message from {name}({phone}, email:{email}): {text}')
        return render(request, 'catalog/contacts.html', self.extra_context)


class ProductDetailView(DetailView):
    """Контроллер просмотра отдельного продукта"""
    model = Product
