from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


from catalog.models import CartItem
from orders.forms import OrderForm
from .models import Order, OrdersProducts


class OrderListView(LoginRequiredMixin, ListView):
    model = Order

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user).prefetch_related('Заказы__product')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        for item in context_data['order_list']:
            context_data[f'products{item.id}'] = [
                product for product in item.products.all()]
        return context_data


class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    form_class = OrderForm

    def form_valid(self, form):
        # Get the current user
        user = self.request.user

        # Create the order instance but don't save it yet
        order = form.save(commit=False)
        order.user = user
        order.total_cost = 0  # Initialize total cost
        order.save()  # Save the order to get an ID for the order

        # Get all cart items for the current user
        cart_items = CartItem.objects.filter(user=user)

        total_cost = 0  # Variable to calculate total cost

        for item in cart_items:
            # Create the relationship between the order and the product
            OrdersProducts.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
            )
            # Update total cost
            # Assuming Product has a price field
            total_cost += item.product.price * item.quantity

            # Delete the cart item
            item.delete()

        # Update the total cost of the order
        order.total_cost = total_cost
        order.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('orders:list')

    def form_invalid(self, form):
        # If the form is invalid, render the form again with errors
        return self.render_to_response({'form': form})


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = CartItem
    success_url = reverse_lazy('catalog:view_cart')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        return context_data
