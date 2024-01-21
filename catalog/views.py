from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory, formset_factory
from django.http import Http404
from django.shortcuts import render, get_object_or_404

from catalog.forms import ProductForm, VersionForm
from catalog.models import Product, Version
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DetailView, DeleteView
from django.urls import reverse_lazy, reverse


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

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = self.object.name
        return context_data


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Добавление продукта'
        VersionFormSet = formset_factory(VersionForm, extra=1)
        context_data['version_formset'] = VersionFormSet()
        return context_data

    def get_success_url(self):
        return reverse('catalog:view', args=[self.kwargs.get('pk')])

    def form_valid(self, form):
        new_product = form.save()
        new_product.owner = self.request.user
        new_product.save()
        selected_version = form.cleaned_data['version']
        selected_version.products.add(new_product)
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:index')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        context_data['title'] = 'Добавление продукта'
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('catalog:view', args=[self.kwargs.get('pk')])


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:index')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Удаление продукта'
        return context_data

    def get_object(self, queryset=None):
        name = self.kwargs.get('name')
        product = get_object_or_404(Product, name=name)
        if product.owner != self.request.user:
            raise Http404

        return product

