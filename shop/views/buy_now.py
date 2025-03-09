from django.shortcuts import redirect, get_object_or_404, render
from shop.models import Product

def buy_now(request, product_id=None):
    cart_items = []
    cart_total = 0

    if product_id:
        # Buying a single product
        product = get_object_or_404(Product, id=product_id)
        cart_items = [{'product': product, 'quantity': 1, 'total_price': product.price}]
        cart_total = product.price
    else:
        # Buying all items from cart
        cart = request.session.get('cart', {})
        if not cart:
            return redirect('cart_view')  # Redirect if cart is empty

        for product_id, quantity in cart.items():
            product = get_object_or_404(Product, id=product_id)
            total_price = product.price * quantity
            cart_items.append({'product': product, 'quantity': quantity, 'total_price': total_price})
            cart_total += total_price

        # Apply discount if available
        if request.session.get('discount_applied', False):
            cart_total = request.session.get('cart_total', cart_total)

    return render(request, 'checkout.html', {'cart_items': cart_items, 'cart_total': cart_total})
