from django.contrib import admin
from profiles.models import *


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'location']
    search_fields = ['user__username']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['product', 'author', 'rating']
    list_filter = ['product']


@admin.register(Favourite)
class FavouriteAdmin(admin.ModelAdmin):
    list_display = ['product', 'user']
    list_filter = ['product']


@admin.register(OrderProduct)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'quantity']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer']


