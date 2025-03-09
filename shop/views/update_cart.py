from django.http import JsonResponse
from shop.models.product import Product

def update_cart(request, product_id, new_quantity):
    # Ensure the quantity is valid (greater than 0)
    if new_quantity < 1:
        return JsonResponse({"error": "Invalid quantity"}, status=400)

    # Get the session cart
    cart = request.session.get('cart', {})

    # Convert product_id to string for consistency in session keys
    product_id = str(product_id)

    try:
        # Get the product object
        product = Product.objects.get(id=int(product_id))

        # If the product exists in the cart, update its quantity
        if product_id in cart:
            cart[product_id] = new_quantity

            # Save updated cart to session
            request.session['cart'] = cart
            request.session.modified = True

            # Calculate new total for the product
            new_total = product.price * new_quantity

            # Recalculate the cart total
            cart_total = sum(Product.objects.get(id=int(pid)).price * qty for pid, qty in cart.items())

            return JsonResponse({
                "success": True,
                "product_name": product.name,
                "new_quantity": new_quantity,
                "new_total": new_total,
                "cart_total": cart_total
            })

        else:
            return JsonResponse({"error": "Product not in cart"}, status=404)

    except Product.DoesNotExist:
        return JsonResponse({"error": "Product not found"}, status=404)
