from django.shortcuts import render, redirect
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, UserUpdateForm, ChangePasswordForm
import requests
from django.contrib.auth.models import User
from django.db.models import Q
import json
from cart.cart import Cart

def search(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        products = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
        if not products:
            messages.warning(request, "Found No Match...")
            return redirect('search')
        else:
            return render(request, 'search.html', {"products": products, "searched": searched})

    else:
        return render(request, 'search.html', {})

def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html', {'categories': categories})

def category_detail(request, slug):
    try:
        category = Category.objects.get(slug=slug)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'category': category, 'products': products})
    except Category.DoesNotExist:
        messages.warning(request, "That Category Does Not Exist!!!")
        return redirect('home')


def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    return render(request, 'product_detail.html', {"product": product})

def home(request):
    products = Product.objects.all().order_by("-id")
    return render(request, 'home.html', {'products': products})

def about(request):
    return render(request, 'about.html', {})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # Do some shopping cart stuff
            current_user = Profile.objects.get(user__id=request.user.id)
            # Get their saved cart from database
            saved_cart = current_user.old_cart
            # Convert database string to python dictionary
            if saved_cart:
                # Convert to dictionary using JSON
                converted_cart = json.loads(saved_cart)
                # add the loaded cart dictionary to our session
                # get the cart
                cart = Cart(request)
                # loop through the cart and add the items from the database
                for key, value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)



            messages.success(request, "You Have Been Logged In!!!")
            return redirect('home')
        else:
            messages.warning(request, "There Was An Error While Logging In, Please Try Again!!!")
            return redirect('login')
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, "You Have Been Logged Out!!!")
    return redirect('login')

def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, "You Have Been Successfully Registered!!! Welcome!")
            return redirect('home')
        else:
            messages.warning(request, "There Was A Problem Registering, PLease Try Again!!!")
            return redirect('register')
    else:
        return render(request, 'register.html', {'form': form})

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UserUpdateForm(request.POST or None, instance=current_user)
        if user_form.is_valid():
            user_form.save()

            login(request, current_user)
            messages.success(request, "User Has Been Updated!!!")
            return redirect('home')
        else:
            for error in user_form.errors.values():
                messages.warning(request, error)
                return redirect('update_user')
        
        # If the user is not POSTing
        return render(request, 'update_user.html', {'user_form': user_form})

    else:
        messages.warning(request, "You Must Be Logged In To View This Page!!!")
        return redirect('login')

def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user

        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.info(request, "Password Has Been Updated Successfully, Please Login Again!!!")
                # We can log in automatically without redirecting us to login page
                # login(request, current_user)
                return redirect('login')
            else:
                for error in form.errors.values():
                    messages.warning(request, error)
                    return redirect('update_password')

        else:
            form = ChangePasswordForm(current_user)
            return render(request, 'update_password.html', {'form': form})
    else:
        messages.warning(request, "You Must Be Logged In To View That Page!!!")
        return redirect('home')

def load_products(request):
    api = requests.get("https://fakestoreapi.com/products")
    products = api.json()

    for product in products:
        category = Category(
            name = product['category']
        )
        category.save()
        Product.objects.create(
            name = product['title'],
            price = product['price'],
            category = category,
            description = product['description'],
            image = product['image'],
        )

