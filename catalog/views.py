from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.forms import inlineformset_factory
from django.http import Http404
from django.shortcuts import render, redirect

from catalog.forms import ProductForm, VersionForm, ModeratorForm
from catalog.models import Product, Version, Category, CartItem
from django.views.generic import TemplateView, CreateView, UpdateView, DetailView, DeleteView, ListView
from django.urls import reverse_lazy, reverse

from catalog.services import category_list_cache


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
        print(
            f'You have new message from {name}({phone}, email:{email}): {text}')
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
        return context_data

    def get_success_url(self):
        messages.success(self.request, 'Отправлено на проверку модерации')
        return reverse('catalog:index')

    def form_valid(self, form):
        new_product = form.save()
        new_product.owner = self.request.user
        new_product.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:index')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if self.object.owner != self.request.user and not user.is_superuser and not user.groups.filter(pk=1):
            raise Http404
        return self.object

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(
            Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(
                self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        if self.request.user.groups.filter(pk=1):
            context_data['moderform'] = ModeratorForm(
                self.request.POST, instance=self.object)
        context_data['title'] = 'Редактирование продукта'
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('catalog:edit', args=[self.kwargs.get('pk')])


@permission_required("users.set_published")
def public_product(request, pk):
    product = Product.objects.get(pk=pk)
    product.is_published = {product.is_published: False,
                            not product.is_published: True}[True]
    product.save()
    return redirect(reverse('catalog:index'))


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:index')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Удаление продукта'
        return context_data

    def get_object(self, queryset=None):
        product = super(ProductDeleteView, self).get_object()
        if not product.owner == self.request.user and not self.request.user.is_superuser:
            raise Http404
        return product


class CategoryListView(ListView):
    model = Category

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['object_list'] = category_list_cache()
        context_data['title'] = 'Категории'
        return context_data


class CategoryDetailView(DetailView):
    model = Category

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['object_list'] = Product.objects.filter(
            category=self.object)
        context_data['title'] = self.object.name
        return context_data


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    fields = ['name', 'description']

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Добавление категории'
        return context_data

    def get_success_url(self):
        return reverse('catalog:category')


class CartView(LoginRequiredMixin, ListView):
    model = CartItem
    template_name = 'catalog/cart.html'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['total_price'] = sum(
            item.product.price * item.quantity for item in context_data['cartitem_list'])
        return context_data


class AddToCartView(LoginRequiredMixin, DetailView):
    model = Product

    def get(self, request, *args, **kwargs):
        product = self.get_object()
        cart_item, created = CartItem.objects.get_or_create(
            product=product, user=request.user)
        cart_item.quantity += 1
        cart_item.save()
        return redirect(self.request.GET.get('next', reverse('catalog:index')))


class RemoveFromCartView(LoginRequiredMixin, DeleteView):
    model = CartItem
    success_url = reverse_lazy('catalog:view_cart')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
