from django.urls import path
from market.views import *

urlpatterns = [
    path('', main_page, name='main_page'),
    path('category/<int:category_id>/', category_page, name='category_page'),
    path('about/', about_page, name='about_page'),
    path('search/', search_page, name='search_page'),
    path('cart/', cart_page, name='cart_page'),
    path('orders_page/<int:user_id>/', orders_page, name='orders_page'),
    path('product/<int:product_id>/', product_page, name='product_page'),
    path('search_results/', search, name='search_results_page'),
    path('checkout/', checkout_page, name='checkout_page'),
    path('wishlist/', wishlist_page, name='wishlist_page')
]