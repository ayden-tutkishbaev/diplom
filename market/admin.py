from django.contrib import admin
from market.models import *


@admin.register(StandardSettings)
class StandardSettingsAdmin(admin.ModelAdmin):
    list_display = ['id', 'main_phone_number']


class WorkingHoursInline(admin.TabularInline):
    model = WorkingHours
    extra = 7


class WorkingDayInline(admin.TabularInline):
    model = WorkingDay
    extra = 1


class WorkingHoursAdmin(admin.ModelAdmin):
    inlines = [WorkingHoursInline]


admin.site.register(WorkingDay, WorkingHoursAdmin)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    search_fields = ['title']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    search_fields = ['title']
    list_filter = ['category']
    # list_editable = ['discount', 'is_featured', 'is_big_featured']


@admin.register(Promo)
class PromoAdmin(admin.ModelAdmin):
    list_display = ['id']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['status', 'phone_number', 'created_at', 'user', 'created_at']
    list_filter = ['status']


@admin.register(Checkout)
class CheckoutAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'email', 'created_at', 'phone_number', 'country',
                    'payment_method'
                    ]
    list_filter = ['country',
                   'status'
                   ]
    search_fields = ['user']


@admin.register(BigFeaturedProduct)
class BigFeaturedProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'product']


@admin.register(SmallFeaturedProducts)
class SmallFeaturedProductsAdmin(admin.ModelAdmin):
    list_display = ['id', 'product']


# UPDATE

@admin.register(Logo)
class LogoAdmin(admin.ModelAdmin):
    list_display = ['id']