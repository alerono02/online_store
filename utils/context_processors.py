from catalog.models import CartItem as Cart


def cart_item_count(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        count = 0 if cart == None else sum(cart.quantity for cart in cart)
    else:
        count = 0
    return {'cart_item_count': count}


def total_cost(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        total_cost = 0 if cart == None else sum(
            cart.product.price * cart.quantity for cart in cart)
    else:
        total_cost = 0
    return {'total_cost': total_cost}


def get_products_from_cart(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        products = [] if cart == None else [cart.product for cart in cart]
    else:
        products = []
    return {'products_from_cart': products}


def delete_cart(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        if cart:
            cart.delete()
