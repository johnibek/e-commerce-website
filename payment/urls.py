from django.urls import path
from . import views

urlpatterns = [
    path('shipping_info/', views.shipping_info, name='shipping_info'),
    path('checkout/', views.checkout, name='checkout'),
]