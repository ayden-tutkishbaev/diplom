from django.db import models
from django.utils.translation import gettext_lazy as _
from market.models import *


class Profile(models.Model):
    name = models.CharField(max_length=150, verbose_name=_("Name of the user"), default='no name')
    location = models.CharField(max_length=150, verbose_name=_("Location of the user"), default='no location')
    phone_number = models.CharField(max_length=150, verbose_name=_("Phone number of the user"),
                                    default='no phone number')

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_("Profile"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")


class Comment(models.Model):
    class RateChoice(models.TextChoices):
        FIVE = 'five', _('5')
        FOUR = 'four', _('4')
        THREE = 'three', _('3')
        TWO = 'two', _('2')
        ONE = 'one', _('1')
        ZERO = 'zero', _('0')

    rating = models.CharField(max_length=20, choices=RateChoice.choices, default=RateChoice.TWO)
    product = models.ForeignKey(Product, verbose_name=_("Product"), on_delete=models.CASCADE)
    author = models.ForeignKey(User, verbose_name=_('User'), on_delete=models.CASCADE)
    text = models.CharField(max_length=100, verbose_name=_('Comment text'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')

    def get_rating_text(self):
        if self.rating == self.RateChoice.FIVE:
            return _("🌟🌟🌟🌟🌟")
        elif self.rating == self.RateChoice.FOUR:
            return _("⭐️⭐️⭐️⭐️")
        elif self.rating == self.RateChoice.THREE:
            return _("⭐️⭐️⭐️")
        elif self.rating == self.RateChoice.TWO:
            return _("⭐️⭐️")
        elif self.rating == self.RateChoice.ONE:
            return _("⭐️")
        elif self.rating == self.RateChoice.ZERO:
            return _("👎")

    def __str__(self):
        return self.author.username


class Favourite(models.Model):
    product = models.ForeignKey(Product, verbose_name=_('Favourite product'), on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name=_('User'), on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'product')
        verbose_name = _('Favourite')
        verbose_name_plural = _('Favourites')


class Order(models.Model):
    customer = models.ForeignKey(Profile, verbose_name=_("Customer"), on_delete=models.SET_NULL, null=True,
                                 blank=True)
    created_at = models.DateTimeField(verbose_name=_("Time of delivery"), auto_now_add=True)

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def __str__(self):
        return f"{self.customer.name} ---> {self.pk}"

    @property
    def get_cart_final_price(self):
        order_products = self.orderproduct_set.all()
        final_price = sum([product.get_total_price for product in order_products])
        return final_price


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_("order"))
    product = models.ForeignKey(Product, verbose_name=_("product"), on_delete=models.CASCADE)
    quantity = models.IntegerField(_("quantity"), default=0, null=True, blank=True)
    added_at = models.DateTimeField(_("created_at"), auto_now_add=True)

    class Meta:
        verbose_name = _("cart item")
        verbose_name_plural = _("cart items")

    def __str__(self):
        return f"Id: {self.id}|Q: {self.quantity}"

    @property
    def get_total_price(self):
        if self.product.discount == 0:
            total_price = self.product.price * self.quantity + self.product.shipping_fee
            return total_price
        else:
            total_price = self.product.discount * self.quantity + self.product.shipping_fee
            return total_price









# class Checkout(models.Model):
#     class PaymentMethod(models.TextChoices):
#         CASH = 'cash', _('Cash')
#         CREDIT_CARD = 'credit_card', _('Credit card')
#
#     name = models.CharField(verbose_name=_("Name of a customer"), max_length=250)
#     phone_number = models.IntegerField(verbose_name=_("Phone number of a customer"))
#     email = models.CharField(verbose_name=_("E-mail of a customer"), max_length=250)
#     payment_method = models.CharField(verbose_name=_("Payment method of a customer"), max_length=100,
#                                       choices=PaymentMethod.choices, default=PaymentMethod.CREDIT_CARD)
#     address = models.CharField(verbose_name=_("Address of a customer"), max_length=250)
#     city = models.CharField(verbose_name=_("City where a customer lives"), max_length=250)
#     country = models.CharField(verbose_name=_("Country where a customer lives"), max_length=250)
#     created_at = models.DateTimeField(verbose_name=_("Create at"), auto_now_add=True)
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         verbose_name = _("Checkout")