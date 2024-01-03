from django.contrib import admin
from .models import Coffee, Cart,Order


# Register your models here.
class CoffeeAdmin(admin.ModelAdmin):
    list_display = ["coffee_id", "coffee_name", "category", "desc", "price", "image"]


class CartAdmin(admin.ModelAdmin):
    list_display = ["coffee_id","qty","userid"]


class OrderAdmin(admin.ModelAdmin):
    list_display = ["order_id","userid","coffee_id","qty"]

admin.site.register(Coffee, CoffeeAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)

