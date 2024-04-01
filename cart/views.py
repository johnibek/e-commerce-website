from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
from django.contrib import messages

def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_products
    quantities = cart.get_quants
    total = cart.total
    return render(request, 'cart_summary.html', {'cart_products': cart_products, 'quantities': quantities, 'total': total})

def cart_add(request):
    # Get the cart
    cart = Cart(request)
    # test for post
    print(request.POST)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        # lookup product in DB
        product = get_object_or_404(Product, id=product_id)

        # save to session
        cart.add(product=product, quantity=product_qty)

        cart_quantity = cart.__len__()


        response = JsonResponse({'quantity': cart_quantity})
        messages.success(request, "You Have Successfully Added An Item To The Cart!!!")
        return response

def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        cart.update(product=product_id, quantity=product_qty)

        messages.success(request, "You Have Successfully Updated The Item!!!")
        return JsonResponse({'quantity': product_qty})

def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))

        cart.delete(product=product_id)

        messages.success(request, "You Have Successfully Deleted The Item!!!")
        return JsonResponse({'product': product_id})

