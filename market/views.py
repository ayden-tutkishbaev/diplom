from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from market.models import *
from profiles.models import *
from profiles.forms import *
from django.contrib import messages
from profiles.utils import *


def main_page(request):
    categories = Category.objects.all()
    newest_products = Product.objects.all().order_by('-created_at')[:6]
    sales_products = Product.objects.filter(discount__gt=0)
    products = Product.objects.all()
    working_hours = WorkingHours.objects.all()
    standard_settings = StandardSettings.objects.get()
    popular_products = Product.objects.filter(is_popular=True)[:6]
    logo = Logo.objects.get()

    bigfeaturedproduct = BigFeaturedProduct.objects.all()
    smallfeaturedproducts = SmallFeaturedProducts.objects.all()

    context = {
        'title': 'Main page',
        'categories': categories,
        'products': products,
        'newest_products': newest_products,
        'sales_products': sales_products,
        'working_hours': working_hours,
        'standard_settings': standard_settings,
        'popular_products': popular_products,
        'bigfeaturedproduct': bigfeaturedproduct,
        'smallfeaturedproducts': smallfeaturedproducts,
        'logo': logo
    }

    return render(request, 'pages/home.html', context)


def search_page(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    working_hours = WorkingHours.objects.all()
    standard_settings = StandardSettings.objects.get()
    logo = Logo.objects.get()

    context = {
        'title': 'Search page',
        'categories': categories,
        'products': products,
        'working_hours': working_hours,
        'standard_settings': standard_settings,
        'logo': logo
    }

    return render(request, 'pages/search_page.html', context)


def search(request):
    working_hours = WorkingHours.objects.all()
    standard_settings = StandardSettings.objects.get()
    search_object = request.GET.get('search')

    products = Product.objects.filter(
        title__iregex=search_object
    )
    categories = Category.objects.all()
    logo = Logo.objects.get()

    context = {
        'title': f'Results of search: {search_object}',
        'categories': categories,
        'products': products,
        'working_hours': working_hours,
        'standard_settings': standard_settings,
        'logo': logo
    }

    return render(request, 'pages/search_page.html', context)


def category_page(request, category_id):
    categories = Category.objects.all()
    products = Product.objects.filter(category=category_id)
    working_hours = WorkingHours.objects.all()
    standard_settings = StandardSettings.objects.get()
    logo = Logo.objects.get()

    context = {
        'title': f'{Category.objects.get(id=category_id)}',
        'categories': categories,
        'products': products,
        'working_hours': working_hours,
        'standard_settings': standard_settings,
        'logo': logo
    }

    return render(request, 'pages/category.html', context)


def product_page(request, product_id):
    categories = Category.objects.all()
    product = Product.objects.get(id=product_id)
    working_hours = WorkingHours.objects.all()
    standard_settings = StandardSettings.objects.get()
    logo = Logo.objects.get()

    comments = Comment.objects.filter(product=product_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.author = request.user
            comment.save()
            messages.success(request, 'Sent!')
            return redirect('product_page', product_id=product_id)
    else:
        form = CommentForm()

    num = 0

    if product.main_pic:
        num += 1
    if product.pic_2:
        num += 1
    if product.pic_3:
        num += 1
    if product.pic_4:
        num += 1

    context = {
        'title': f'{product.title}',
        'product': product,
        'categories': categories,
        'working_hours': working_hours,
        'standard_settings': standard_settings,
        'images_num': num,
        'form': form,
        'comments': comments,
        'logo': logo
    }

    if request.user.is_authenticated:
        favorites = Favourite.objects.filter(user=request.user).values_list('product_id', flat=True)
        context.update({
            'favorites': favorites
        })

    return render(request, 'pages/product.html', context)


@login_required(login_url='login_page')
def about_page(request):

    categories = Category.objects.all()
    products = Product.objects.all()
    working_hours = WorkingHours.objects.all()
    standard_settings = StandardSettings.objects.get()
    promo = Promo.objects.get()
    logo = Logo.objects.get()

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.user = request.user
            message.save()
            messages.success(request, 'Message saved successfully!')
            return redirect('about_page')
        else:
            messages.error(request, 'Form is not valid.')
    else:
        form = MessageForm()

    context = {
        'title': 'About us',
        'categories': categories,
        'products': products,
        'working_hours': working_hours,
        'standard_settings': standard_settings,
        'form': form,
        'promo': promo,
        'logo': logo
    }

    return render(request, 'pages/about.html', context)


@login_required(login_url='login_page')
def cart_page(request):

    cart_info = get_cart_data(request)

    categories = Category.objects.all()
    working_hours = WorkingHours.objects.all()
    standard_settings = StandardSettings.objects.get()
    logo = Logo.objects.get()

    context = {
        'title': 'Cart',
        'categories': categories,
        'working_hours': working_hours,
        'standard_settings': standard_settings,
        'order': cart_info['order'],
        'products': cart_info['products'],
        'cart_total_price': cart_info['cart_total_price'],
        'logo': logo
    }

    return render(request, 'pages/cart.html', context)


@login_required(login_url='login_page')
def checkout_page(request):

    cart_info = get_cart_data(request)

    categories = Category.objects.all()
    working_hours = WorkingHours.objects.all()
    standard_settings = StandardSettings.objects.get()
    logo = Logo.objects.get()

    if request.method == 'POST':
        form = CheckoutForm(data=request.POST)

        if form.is_valid():
            checkout = form.save(commit=False)
            checkout.user = request.user
            checkout.total_price = cart_info['cart_total_price']
            checkout.save()
            messages.success(request, 'Your checkout request has been sent successfully! Now you can pay your order.')
            return redirect('payment')
        else:
            for field in form.errors:
                messages.error(request, form.errors[field].as_text())
            return redirect('checkout_page')
    else:
        form = CheckoutForm()


    context = {
        'title': 'Checkout',
        'categories': categories,
        'working_hours': working_hours,
        'standard_settings': standard_settings,
        'form': form,
        'order': cart_info['order'],
        'products': cart_info['products'],
        'cart_total_price': cart_info['cart_total_price'],
        'logo': logo
    }

    return render(request, 'pages/checkout.html', context)


@login_required(login_url='login_page')
def orders_page(request, user_id):
    categories = Category.objects.all()
    working_hours = WorkingHours.objects.all()
    standard_settings = StandardSettings.objects.get()
    user_id = request.user.id
    user = User.objects.get(id=user_id)

    orders = Checkout.objects.filter(user=user)

    cart_info = get_cart_data(request)
    logo = Logo.objects.get()


    context = {
        'title': 'Orders',
        'categories': categories,
        'working_hours': working_hours,
        'standard_settings': standard_settings,
        'order': cart_info['order'],
        'products': cart_info['products'],
        'cart_total_price': cart_info['cart_total_price'],
        'orders': orders,
        'logo': logo
    }

    return render(request, 'pages/orders.html', context)


@login_required(login_url='login_page')
def wishlist_page(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    working_hours = WorkingHours.objects.all()
    standard_settings = StandardSettings.objects.get()
    favourites = Favourite.objects.filter(user=request.user)
    logo = Logo.objects.get()

    context = {
        'title': 'Wishlist',
        'categories': categories,
        'products': products,
        'working_hours': working_hours,
        'standard_settings': standard_settings,
        'favourites': favourites,
        'logo': logo
    }

    return render(request, 'pages/wishlist.html', context)