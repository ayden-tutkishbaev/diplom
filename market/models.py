from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class StandardSettings(models.Model):
    all_rights_reserved = models.CharField(_('All rights reserved'), max_length=300)
    main_email = models.CharField(_('Main email'), max_length=150)
    main_phone_number = models.CharField(max_length=100, verbose_name=_('Main Phone Number'))

    class Meta:
        verbose_name = _('Standard settings')

    def clean(self):
        count = StandardSettings.objects.count()
        max_records = 0

        if count > max_records:
            raise ValidationError(_("You can add only one recording!"))

    def __str__(self):
        return self.all_rights_reserved


class WorkingDay(models.Model):
    title = models.CharField(_('Title'), max_length=50, default='working day')

    class Meta:
        verbose_name = _('Working hours')

    def __str__(self):
        return self.title


class WorkingHours(models.Model):
    class WeekChoice(models.TextChoices):
        MONDAY = 'Monday', _('Monday')
        TUESDAY = 'Tuesday', _('Tuesday')
        WEDNESDAY = 'Wednesday', _('Wednesday')
        THURSDAY = 'Thursday', _('Thursday')
        FRIDAY = 'Friday', _('Friday')
        SATURDAY = 'Saturday', _('Saturday')
        SUNDAY = 'Sunday', _('Sunday')

    working_day = models.ForeignKey(WorkingDay, on_delete=models.CASCADE)
    week_day = models.CharField(max_length=50, verbose_name=_('Day'), choices=WeekChoice.choices)
    start = models.CharField(max_length=30, verbose_name=_('Start hour'))
    finish = models.CharField(max_length=30, verbose_name=_('Finish hour'))

    class Meta:
        verbose_name = _('Working hours')

    def clean(self):
        count = WorkingDay.objects.count()
        max_records = 0

        if count > max_records:
            raise ValidationError(_("You can add only one recording!"))

    def __str__(self):
        return self.week_day


class Category(models.Model):
    title = models.CharField(verbose_name=_('Title'), max_length=150)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(_('Title'), max_length=150)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_('Product category'),
                                 related_name='product_category')

    quantity = models.IntegerField(_('Quantity'), default=1)

    main_pic = models.ImageField(upload_to='product_images/', blank=True, null=True, verbose_name=_('Main product picture'))
    pic_2 = models.ImageField(upload_to='product_images/', blank=True, null=True, verbose_name=_('Second product picture'))
    pic_3 = models.ImageField(upload_to='product_images/', blank=True, null=True, verbose_name=_('Third product picture'))
    pic_4 = models.ImageField(upload_to='product_images/', blank=True, null=True, verbose_name=_('Fourth product picture'))

    price = models.FloatField(verbose_name=_('Product price'))
    discount = models.FloatField(verbose_name=_('Product discount'), default=0)

    shipping_fee = models.FloatField(verbose_name=_('Product shipping fee'), default=0)

    in_stock = models.BooleanField(verbose_name=_('In stock?'), default=True)
    is_popular = models.BooleanField(verbose_name=_("Is popular?"), default=False)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Product created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Product updated at"))
    description = models.TextField(_("Description"))

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        return self.title


class Promo(models.Model):
    image = models.ImageField(_("Image"), upload_to='promo/')

    class Meta:
        verbose_name = _("Promo")
        verbose_name_plural = _("Promos")


class Checkout(models.Model):
    class DeliveryStatus(models.TextChoices):
        ACCEPTED = 'accepted', _('Accepted')
        PENDING = 'pending', _('Pending')
        DELIVERED = 'delivered', _('Delivered')
        CANCELLED = 'cancelled', _('Cancelled')

    class PaymentMethod(models.TextChoices):
        CREDIT_CARD = 'credit_card', _('Credit card')

    name = models.CharField(verbose_name=_("Name of a customer"), max_length=250)
    phone_number = models.IntegerField(verbose_name=_("Phone number of a customer"))
    email = models.CharField(verbose_name=_("E-mail of a customer"), max_length=250)
    payment_method = models.CharField(verbose_name=_("Payment method of a customer"), max_length=100,
                                      choices=PaymentMethod.choices, default=PaymentMethod.CREDIT_CARD)
    address = models.CharField(verbose_name=_("Address of a customer"), max_length=250)
    city = models.CharField(verbose_name=_("City where a customer lives"), max_length=250)
    country = models.CharField(verbose_name=_("Country where a customer lives"), max_length=250)

    status = models.CharField(verbose_name=_("Status of a customer"), max_length=100, choices=DeliveryStatus.choices,
                              default=DeliveryStatus.ACCEPTED)

    created_at = models.DateTimeField(verbose_name=_("Time of delivery"), auto_now_add=True)

    total_price = models.FloatField(default=0, verbose_name=_("Total price"))

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ordered_By',
                             verbose_name=_("Ordered by"))

    class Meta:
        verbose_name = _("Checkout")

    def __str__(self):
        return self.name

    def get_pay_method(self):
        if self.payment_method == self.PaymentMethod.CREDIT_CARD:
            return _("Credit card  ")

    @property
    def cart_final_price(self):
        order_products = self.cartitem_set.all()
        final_price = sum([product.total_price for product in order_products])
        return final_price


class Message(models.Model):
    class MessageStatus(models.TextChoices):
        PENDING = 'sent', _("Sent")
        ANSWERED = 'answered', _("Answered")

    status = models.CharField(verbose_name=_("Status of a message"), max_length=50, choices=MessageStatus.choices,
                              default=MessageStatus.PENDING, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_author',
                             verbose_name=_("Author of the message"))
    phone_number = models.CharField(verbose_name=_("Phone number"), max_length=20)
    text = models.TextField(verbose_name=_("Text"))
    created_at = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True)

    def __str__(self):
        return self.phone_number

    class Meta:
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")


class BigFeaturedProduct(models.Model):
    product = models.ForeignKey(Product, verbose_name=_("Big featured product"), on_delete=models.SET_NULL, null=True,
                                blank=True)

    def clean(self):
        count = BigFeaturedProduct.objects.count()
        max_records = 0

        if count > max_records:
            raise ValidationError(_("You can add only one recording!"))

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = _("Big featured product")
        verbose_name_plural = _("Big featured products")


class SmallFeaturedProducts(models.Model):
    product = models.ForeignKey(Product, verbose_name=_("Big featured product"), on_delete=models.SET_NULL, null=True,
                                blank=True)

    def clean(self):
        count = SmallFeaturedProducts.objects.count()
        max_records = 2

        if count > max_records:
            raise ValidationError(_("You can add only 3 recordings!"))

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = _("Small featured product")
        verbose_name_plural = _("Small featured products")


# UPDATE

class Logo(models.Model):
    image = models.ImageField(_("Image"), upload_to='logo/')

    class Meta:
        verbose_name = _("Logo")
        verbose_name_plural = _("Logos")