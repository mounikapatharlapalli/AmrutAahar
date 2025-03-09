from django.shortcuts import render
from shop.models import Product, Category, Wishlist

def product_list(request):
    # Get category and price filter values from GET request
    category_id = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    # Get all categories for sidebar menu
    categories = Category.objects.all()

    # Initialize querysets and variables
    selected_category = None
    products = Product.objects.all()

    # ✅ Filter products by category
    if category_id and category_id.isdigit():  # Ensure it's a valid numeric ID
        selected_category = Category.objects.filter(id=category_id).first()
        if selected_category:
            products = products.filter(category=selected_category)

    # ✅ Filter products by price range
    try:
        # Only apply filter if both prices are provided
        if min_price and max_price:
            min_price_int = int(min_price)
            max_price_int = int(max_price)

            # Apply price range filtering
            products = products.filter(price__gte=min_price_int, price__lte=max_price_int)
    except ValueError:
        # If min_price or max_price can't be converted to int, ignore filtering
        pass

    # ✅ Wishlist product IDs
    if request.user.is_authenticated:
        wishlist_product_ids = list(Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True))
    else:
        wishlist_product_ids = request.session.get('wishlist', [])

    # ✅ Render the product list page with context
    return render(request, "product_list.html", {
        "products": products,                     # Filtered products
        "categories": categories,                 # All categories for sidebar
        "selected_category": selected_category,   # Current selected category
        "min_price": min_price,                   # Retain filter values in form
        "max_price": max_price,
        "wishlist_product_ids": wishlist_product_ids,  # Pass to template ✅
    })
