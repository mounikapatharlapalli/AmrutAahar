from django.http import JsonResponse
from shop.models.product import Product  
import json

def apply_discount(request):
    if request.method == "POST":
        data = json.loads(request.body)
        discount_code = data.get('discount_code', '')

        valid_discount_codes = {
            'AA15': 0.15,  # 15% discount
            'FUAA20': 0.20,  # 20% discount
        }

        if discount_code not in valid_discount_codes:
            return JsonResponse({"success": False, "message": "Invalid discount code"})

        discount_percentage = valid_discount_codes[discount_code]
        cart = request.session.get('cart', {})

        if not cart:
            return JsonResponse({"success": False, "message": "No items in the cart"})

        # Calculate cart total
        cart_total = sum(Product.objects.get(id=int(pid)).price * quantity for pid, quantity in cart.items())
        new_cart_total = cart_total * (1 - discount_percentage)

        # Store new cart total & discount details in session
        request.session['cart_total'] = new_cart_total
        request.session['discount_applied'] = True
        request.session['discount_code'] = discount_code
        request.session.modified = True

        return JsonResponse({"success": True, "new_cart_total": new_cart_total})
