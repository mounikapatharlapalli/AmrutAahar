from django.shortcuts import render, redirect
from django.contrib import messages
from shop.models import Product
from datetime import datetime, timedelta
from django.http import JsonResponse
import json
from django.contrib.auth.decorators import login_required
def checkout(request):
   
    cart = request.session.get('cart', {})
    cart_items = []
    cart_total = 0

    for product_id, quantity in cart.items():
        product = Product.objects.filter(id=product_id).first()
        if product:
            total_price = product.price * quantity
            cart_items.append({'product': product, 'quantity': quantity, 'total_price': total_price})
            cart_total += total_price

    # Apply discount if available
    if request.session.get('discount_applied', False):
        cart_total = request.session.get('cart_total', cart_total)

    # Calculate expected delivery date (5 days from today)
    expected_delivery = (datetime.now() + timedelta(days=5)).strftime("%d %B %Y")

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'expected_delivery': expected_delivery
    })


def order_confirmation(request):
   

    return render(request, 'order_confirmation.html')


def store_order_details(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            # ✅ Store order details in session
            request.session['order_details'] = {
                'name': data.get('name', 'Customer'),
                'phone': data.get('phone', ''),
                'address': data.get('address', ''),
                'city': data.get('city', ''),
                'pincode': data.get('pincode', ''),
                'state': data.get('state', ''),
                'country': data.get('country', ''),
                'payment_id': data.get('razorpay_payment_id', ''),
                'expected_delivery': (datetime.now() + timedelta(days=5)).strftime("%d %B %Y")
            }

            request.session.modified = True  # Ensures session is saved
            return JsonResponse({"success": True, "redirect_url": "/order-confirmation/"})
        
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Invalid request"})


def order_success(request):
    order_details = request.session.get('order_details', None)

    if not order_details:
        messages.error(request, "No recent order found.")
        return redirect("home")  # Redirect to homepage if no order data

    return render(request, 'order_confirmation.html', {'order_details': order_details})
