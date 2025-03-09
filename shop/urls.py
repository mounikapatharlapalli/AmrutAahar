from django.urls import path
from .views.home import HomeView
from .views.login import SignInView
from .views.signup import SignUpView
from .views.logout import logout_user
from .views import product_detail, buy_now, add_to_cart
from .views.cart_views import cart_view, remove_from_cart
from .views.place_order import place_order
from .views.update_cart import update_cart  # Adjusted
from shop.views.apply_discount import apply_discount  # Adjusted
from .views.order_views import checkout_view,order_success
from shop.views.checkout import order_confirmation,store_order_details
from shop.views.filter import product_list
from shop.views.about_us import about_us
from shop.views.wishlist import wishlist_view,add_to_wishlist,remove_from_wishlist
from shop.views.success import success

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('logout/', logout_user, name='logout'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart_view, name='cart_view'),
    path('cart/remove/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/buy_now/', buy_now, name='buy_now'),  # Checkout for full cart
    path('product/<int:product_id>/buy_now/', buy_now, name='buy_now'),
    path('checkout/', checkout_view, name='checkout'),
    path('order/place/', place_order, name='place_order'),
    path('order/success/', order_success, name='order_success'),

    
    # Update the cart by changing product quantity in the order
    path('update_cart/<int:product_id>/<int:new_quantity>/', update_cart, name='update_cart'),  # Adjusted to directly use update_cart view
    
    # Apply discount code to the user's order
     path("apply_discount/", apply_discount, name="apply_discount"),
     path('order-confirmation/', order_success, name='order_success'),  # Order success page
    path('order-confirmation/', order_confirmation, name='order_confirmation'),  # Save order details
    path('store-order-details/', store_order_details, name='store_order_details'),
     path('product_list', product_list, name='product_list'),
     path('about_us/',about_us,name="about_us"),
     path('wishlist/', wishlist_view, name='wishlist_view'),
    path('wishlist/add/<int:product_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', remove_from_wishlist, name='remove_from_wishlist'),
    path('success/',success,name='success'),
    ]
