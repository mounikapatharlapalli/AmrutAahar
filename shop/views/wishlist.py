from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from shop.models import Product, Wishlist

# View Wishlist
def wishlist_view(request):
    if request.user.is_authenticated:
        wishlist_items = Wishlist.objects.filter(user=request.user)
    else:
        wishlist_product_ids = request.session.get('wishlist', [])
        wishlist_items = Product.objects.filter(id__in=wishlist_product_ids)

    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})

# Add to Wishlist (AJAX & Non-AJAX)
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
        Wishlist.objects.get_or_create(user=request.user, product=product)
        wishlist_count = Wishlist.objects.filter(user=request.user).count()
    else:
        wishlist = request.session.get('wishlist', [])
        if product_id not in wishlist:
            wishlist.append(product_id)
            request.session['wishlist'] = wishlist
        wishlist_count = len(request.session['wishlist'])

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'added', 'wishlist_count': wishlist_count})
    
    return redirect('wishlist_view')

# Remove from Wishlist (AJAX & Non-AJAX)
def remove_from_wishlist(request, product_id):
    if request.user.is_authenticated:
        Wishlist.objects.filter(user=request.user, product_id=product_id).delete()
        wishlist_count = Wishlist.objects.filter(user=request.user).count()
    else:
        wishlist = request.session.get('wishlist', [])
        if product_id in wishlist:
            wishlist.remove(product_id)
            request.session['wishlist'] = wishlist
        wishlist_count = len(request.session.get('wishlist', []))

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'removed', 'wishlist_count': wishlist_count})

    return redirect('wishlist_view')
