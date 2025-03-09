from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from shop.models import Product
from shop.views.apply_discount import apply_discount
import json

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Ensure cart exists and is a dictionary
    cart = request.session.get('cart', {})

    # Convert product_id to string for consistency in session keys
    product_id = str(product_id)

    # Initialize product quantity if not already in cart
    cart[product_id] = cart.get(product_id, 0) + 1

    # Save cart to session
    request.session['cart'] = cart
    request.session.modified = True  # Ensure session is updated

    messages.success(request, f"{product.name} added to cart!")
    return redirect('product_detail', product_id=product.id)

def cart_view(request):
    cart = request.session.get('cart', {})

    cart_items = []
    cart_total = 0

    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=int(product_id))  # Convert back to int
        except Product.DoesNotExist:
            continue  # Skip if product was deleted

        total_price = product.price * quantity
        cart_items.append({'product': product, 'quantity': quantity, 'total_price': total_price})
        cart_total += total_price

    # Handle discount code form submission
    if request.method == "POST" and 'discount_code' in request.POST:
        discount_code = request.POST['discount_code']
        response = apply_discount(request, discount_code)
        
        # Handle the response from apply_discount
        if response.status_code == 200:
            data = json.loads(response.content)
            if data['success']:
                cart_total = data['new_cart_total']
                messages.success(request, f"Discount applied! New total: {cart_total}")
            else:
                messages.error(request, data['message'])
        else:
            messages.error(request, "Failed to apply discount")

    return render(request, 'cart.html', {'cart_items': cart_items, 'cart_total': cart_total})

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})

    product_id = str(product_id)  # Ensure product ID is a string for session keys

    if product_id in cart:
        del cart[product_id]
        request.session['cart'] = cart
        request.session.modified = True  # Ensure session saves the change

    messages.success(request, "Item removed from cart.")
    return redirect('cart_view')
