from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem

admin.site.register([ShippingAddress, Order, OrderItem])
