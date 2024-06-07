from django.urls import path
from profiles.views import *

urlpatterns = [
    path('register/', register_page, name='register_page'),
    path('login/', login_page, name='login_page'),
    path('logout/', user_logout, name='logout'),
    path('profile/<int:user_id>/', profile, name='your_profile'),
    path('add_to_favorites/<int:product_id>/', add_to_favorites, name='add_to_favorites'),
    path('remove_from_favorites/<int:product_id>/', remove_from_favorites, name='remove_from_favorites'),
    path('edit_profile/<int:user_id>/', edit_profile, name='edit_profile'),
    path('to_cart/<int:product_id>/<str:action>/', to_cart, name='to_cart'),

    path('payment/', create_payment_session, name='payment_session'),
    path('payment_success/', success, name='payment_success'),
    path('payment', payment, name='payment')
]