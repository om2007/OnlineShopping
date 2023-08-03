from django.contrib import admin
from .models import Customer, Product, Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['product', 'customer', 'customer_address', 'customer_phone_number', 'date_ordered', 'status', 'id']


admin.site.register(Customer)
admin.site.register(Product)

