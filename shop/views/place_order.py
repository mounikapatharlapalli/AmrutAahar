from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from shop.models import Order

def place_order(request):
    if request.method == "POST":
        if 'customer_id' not in request.session:
            return redirect(f"/signin/?next=/checkout/")

        cart = request.session.get('cart', {})
        customer_id = request.session.get('customer_id')

        if cart:
            for product_id, quantity in cart.items():
                Order.objects.create(
                    product_id=product_id,
                    user_id=customer_id,
                    quantity=quantity
                )
            request.session['cart'] = {}  # Clear cart after placing order
            messages.success(request, "Your order has been placed successfully!")
        else:
            messages.error(request, "Your cart is empty!")

        return redirect('order_success')
    
    return redirect('cart_view')
