import re
from market.models import *
from profiles.models import *


def phone_number_validation(phone_number):
    pattern = re.compile(r"^\+?[1-9]\d{11}")
    return bool(pattern.match(phone_number))


class CartForAuthenticatedUser:
    def __init__(self, request, product_id=None, action=None):
        self.user = request.user

        if product_id and action:
            self.add_or_delete(product_id, action)

    def get_cart_info(self):
        customer, created = Profile.objects.get_or_create(
            user=self.user
        )

        order, created = Order.objects.get_or_create(
            customer=customer
        )

        order_products = order.orderproduct_set.all()
        cart_total_price = order.get_cart_final_price

        return {
            'cart_total_price': cart_total_price,
            'order': order,
            'products': order_products
        }

    def add_or_delete(self, product_id, action):
        order = self.get_cart_info()['order']
        product = Product.objects.get(pk=product_id)
        order_product, created = OrderProduct.objects.get_or_create(
            order=order, product=product
        )

        if action == 'add':
            order_product.quantity += 1
            product.quantity -= 1
        else:
            order_product.quantity -= 1
            product.quantity += 1
        # elif action == 'delete_all':
        #     order_products = order.orderproduct_set.all()
        #     products = product.product_set.all()
        #     for product in order_products:
        #         product.quantity -= 1
        #     for product in products:
        #         product.quantity += 1

        product.save()
        order_product.save()

        if order_product.quantity <= 0:
            order_product.delete()

    def clear(self):
        order = self.get_cart_info()['order']
        order_products = order.orderproduct_set.all()
        for product in order_products:
            product.delete()
        order.save()


def get_cart_data(request):
    cart = CartForAuthenticatedUser(request)
    cart_info = cart.get_cart_info()

    return {
        'cart_total_price': cart_info['cart_total_price'],
        'order': cart_info['order'],
        'products': cart_info['products']
    }

