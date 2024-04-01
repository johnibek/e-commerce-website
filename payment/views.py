from django.shortcuts import render, redirect
from .forms import ShippingForm
from django.contrib import messages
from .models import ShippingAddress
from cart.views import Cart
from .forms import ShippingForm

def shipping_info(request):
    shipping_addresses = ShippingAddress.objects.all()
    if request.user.is_authenticated:
        users = []
        for shipping_address in shipping_addresses:
            users.append(shipping_address.user)

        if request.user not in users:
            if request.method == 'POST':
                form = ShippingForm(request.POST)
                if form.is_valid():
                    shipping_detail = form.save(commit=False)
                    shipping_detail.user = request.user
                    shipping_detail.save()
                    messages.success(request, "Shipping Info Has Been Saved Successfully")
                    return redirect('home')
            else:
                form = ShippingForm()
                return render(request, 'payment/shipping_info.html', {'form': form})
        else:
            shipping_detail = ShippingAddress.objects.get(user=request.user)
            if request.method == 'POST':
                form = ShippingForm(request.POST, instance=shipping_detail)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Shipping Info Has Been Updated Successfully")
                    return redirect('home')

            else:
                form = ShippingForm(instance=shipping_detail)
                return render(request, 'payment/shipping_info.html', {'form': form})

    else:
        messages.warning(request, "You Must Be Logged In To View This Page!!!")
        return redirect('home')

def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_products()
    quantities = cart.get_quants()
    total = cart.total()

    if request.user.is_authenticated:
        shipping_user = ShippingAddress.objects.get(user=request.user)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        context = {
            'cart_products': cart_products,
            'quantities': quantities,
            'total': total,
            'shipping_form': shipping_form,
            'shipping_info': shipping_user
        }
        return render(request, 'payment/checkout.html', context)

    else:
        shipping_form = ShippingForm(request.POST or None)
        context = {
            'cart_products': cart_products,
            'quantities': quantities,
            'total': total,
            'shipping_form': shipping_form
        }

        return render(request, 'payment/checkout.html', context)
