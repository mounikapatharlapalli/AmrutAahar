from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Product, Order

@login_required
def checkout_view(request):
    """ Display the checkout page with cart details """
    cart = request.session.get('cart', {})

    if not cart:
        messages.error(request, "Your cart is empty!")
        return redirect('cart_view')

    cart_items = []
    cart_total = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        total_price = product.price * quantity
        cart_items.append({'product': product, 'quantity': quantity, 'total_price': total_price})
        cart_total += total_price

    return render(request, 'shop/checkout.html', {'cart_items': cart_items, 'cart_total': cart_total})

@login_required
def place_order(request):
    """ Handles order placement and clears the cart """
    if request.method == "POST":
        cart = request.session.get('cart', {})

        if not cart:
            messages.error(request, "Your cart is empty!")
            return redirect('cart_view')

        # Create an order for each cart item
        for product_id, quantity in cart.items():
            product = get_object_or_404(Product, id=product_id)
            Order.objects.create(product=product, user=request.user, quantity=quantity)

        # Clear cart after order placement
        request.session['cart'] = {}
        messages.success(request, "Your order has been placed successfully!")
        return redirect('order_success')

    return redirect('cart_view')

@login_required
def order_success(request):
    """ Display order success page """
    return render(request, 'shop/order_success.html')
