from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Order
from django.http import JsonResponse
from .models import CartItem, Product

# Display all products
def product_list(request):
    min_price = request.GET.get('min_price', 0)  # Default min price
    max_price = request.GET.get('max_price', 10000)  # Default max price

    # Filter products based on price range
    products = Product.objects.filter(price__gte=min_price, price__lte=max_price)

    return render(request, 'product_list.html', {
        'products': products,
        'min_price': min_price,
        'max_price': max_price
    })


# Display product details
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})

# Order success page
@login_required
def order_success(request):
    return render(request, 'order_success.html')


def update_cart(request, product_id, new_quantity):
    # Ensure the quantity is valid (greater than 0)
    if new_quantity < 1:
        return JsonResponse({"error": "Invalid quantity"}, status=400)
    
    try:
        # Ensure the user is authenticated and retrieve the user's cart item
        if request.user.is_authenticated:
            # Get the user's cart (assuming you have a Cart model)
            cart_item = CartItem.objects.get(product_id=product_id, cart__user=request.user)
            
            # Update the quantity of the product in the cart
            cart_item.quantity = new_quantity
            cart_item.save()

            # Calculate the new total price for the updated item
            product = cart_item.product
            new_total = product.price * cart_item.quantity

            # Recalculate the cart total
            cart_items = CartItem.objects.filter(cart__user=request.user)
            cart_total = sum(item.product.price * item.quantity for item in cart_items)

            return JsonResponse({
                "new_quantity": cart_item.quantity,
                "new_total": new_total,
                "cart_total": cart_total
            })
        else:
            return JsonResponse({"error": "User not authenticated"}, status=401)
        
    except CartItem.DoesNotExist:
        return JsonResponse({"error": "Cart item not found"}, status=404)

