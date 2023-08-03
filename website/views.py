from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from .forms import *
from .models import Product, Cart
from django.http import HttpResponse
from django.urls import reverse


# Create your views here.

def home(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'website/home.html', context)


# def placeOrder(request, i):
#     customer = Customer.objects.get(id=i)
#     form = createorderform(instance=customer)
#     if request.method == 'POST':
#         form = createorderform(request.POST, instance=customer)
#         if form.is_valid():
#             form.save()
#             return redirect('/')
#     context = {'form': form}
#     return render(request, 'website/placeOrder.html', context)

def placeOrder(request, i):
    if request.method == "POST":
        # Retrieve the product based on the id
        product = get_object_or_404(Product, id=i)

        # Retrieve the customer based on the current user
        customer = get_object_or_404(Customer, user=request.user)

        # Create a new Order with the product and customer
        Order.objects.create(product=product, customer=customer, status='PENDING')

        # Get the user's cart and remove the product from it
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart.products.remove(product)

        return redirect('paymentComplete')
    else:
        # Get or create the user's cart
        cart, created = Cart.objects.get_or_create(user=request.user)
        context = {
            'cart': cart,
        }
        return render(request, 'website/placeOrder.html', context)


def addProduct(request):
    form = createproductform()
    if request.method == 'POST':
        form = createproductform(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'website/addProduct.html', context)


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = createuserform()
        customerform = createcustomerform()
        if request.method == 'POST':
            form = createuserform(request.POST)
            customerform = createcustomerform(request.POST)
            if form.is_valid() and customerform.is_valid():
                user = form.save()
                customer = customerform.save(commit=False)
                customer.user = user
                customer.save()
                return redirect('login')
        context = {
            'form': form,
            'customerform': customerform,
        }
        return render(request, 'website/register.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
        context = {}
        return render(request, 'website/login.html', context)


def logoutPage(request):
    logout(request)
    return redirect('/')


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart.products.add(product)
    return redirect('home')


def removeFromCart(request, i):
    if request.method == "POST":
        product = get_object_or_404(Product, id=i)
        cart = Cart.objects.get(user=request.user)
        cart.products.remove(product)
        return redirect('/')


def paymentComplete(request):
    return render(request, 'website/paymentDone.html')


def about(request):
    return render(request, 'website/about.html')
