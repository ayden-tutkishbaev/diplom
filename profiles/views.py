import stripe
from django.shortcuts import render, redirect
from django.urls import reverse

from config import settings
from market.models import *
from profiles.models import *
from profiles.forms import *
from django.contrib.auth import logout, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from profiles.utils import *
import stripe


def register_page(request):

    categories = Category.objects.all()
    products = Product.objects.all()
    working_hours = WorkingHours.objects.all()
    standard_settings = StandardSettings.objects.get()
    logo = Logo.objects.get()


    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            profile_user = Profile.objects.create(user=user)
            profile_user.save()
            login(request, user)
            messages.success(request, 'Registered successfully!')
            return redirect('main_page')
        else:
            for field in form.errors:
                messages.error(request, form.errors[field].as_text())
            return redirect('register_page')
    else:
        form = RegisterForm()

    context = {
        'title': 'Register',
        'categories': categories,
        'products': products,
        'working_hours': working_hours,
        'standard_settings': standard_settings,
        'form': form,
        'logo': logo

    }

    return render(request, 'pages/register.html', context)


def login_page(request):

    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user:
                login(request, user)
                messages.success(request, 'Logged in!')
                return redirect('main_page')
            else:
                for field in form.errors:
                    messages.error(request, form.errors[field].as_text())
                return redirect('login_page')
        else:
            for field in form.errors:
                messages.error(request, form.errors[field].as_text())
            return redirect('login_page')
    else:
        form = LoginForm()

    categories = Category.objects.all()
    products = Product.objects.all()
    working_hours = WorkingHours.objects.all()
    standard_settings = StandardSettings.objects.get()
    logo = Logo.objects.get()

    context = {
        'title': 'Login',
        'categories': categories,
        'products': products,
        'working_hours': working_hours,
        'standard_settings': standard_settings,
        'form': form,
        'logo': logo
    }

    return render(request, 'pages/login.html', context)


def user_logout(request):
    logout(request)
    messages.info(request, 'Logged out!')
    return redirect('main_page')


@login_required(login_url='login_page')
def edit_profile(request, user_id):
    user = User.objects.get(id=user_id)
    user_profile = Profile.objects.get(user=user)

    categories = Category.objects.all()
    products = Product.objects.all()
    working_hours = WorkingHours.objects.all()
    standard_settings = StandardSettings.objects.get()
    logo = Logo.objects.get()

    if request.method == 'POST':
        user_form = UserForm(instance=user,
                             data=request.POST)
        profile_form = ProfileForm(instance=user_profile,
                                   data=request.POST,
                                   files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Updated successfully!')
            return redirect('your_profile', user.id)
        else:
            for field in user_form.errors:
                messages.error(request, user_form.errors[field].as_text())
            for field in profile_form.errors:
                messages.error(request, profile_form.errors[field].as_text())
            return redirect('edit_profile', user.id)
    else:
        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=user_profile)

    context = {
        'title': 'Profile',
        'categories': categories,
        'products': products,
        'working_hours': working_hours,
        'standard_settings': standard_settings,
        'user_form': user_form,
        'profile_form': profile_form,
        'user_profile': user_profile,
        'user': user,
        'logo': logo
    }

    return render(request, 'pages/edit_profile.html', context)


def profile(request, user_id):
    user = User.objects.get(id=user_id)
    user_profile = Profile.objects.get(user=user)

    categories = Category.objects.all()
    products = Product.objects.all()
    working_hours = WorkingHours.objects.all()
    standard_settings = StandardSettings.objects.get()

    favourites = Favourite.objects.filter(user=user)
    logo = Logo.objects.get()


    context = {
        'title': 'Your profile',
        'categories': categories,
        'products': products,
        'working_hours': working_hours,
        'standard_settings': standard_settings,
        'user': user,
        'favourites': favourites,
        'user_profile': user_profile,
        'logo': logo
    }

    return render(request, 'pages/profile.html', context)


@login_required(login_url='login_page')
def add_to_favorites(request, product_id):
    product = Product.objects.get(pk=product_id)
    favorite, created = Favourite.objects.get_or_create(user=request.user, product=product)
    return redirect('wishlist_page')


@login_required(login_url='login_page')
def remove_from_favorites(request, product_id):
    product = Product.objects.get(pk=product_id)
    favorite = Favourite.objects.get(user=request.user, product=product)
    favorite.delete()
    return redirect('wishlist_page')


def to_cart(request, product_id, action):
    if request.user.is_authenticated:
        CartForAuthenticatedUser(request, product_id, action)
        return redirect('cart_page')
    else:
        # TODO: error
        return redirect('login_page')


def create_payment_session(request):
    if request.method == 'POST':
        stripe.api_key = settings.STRIPE_SECRET_KEY
        user_cart = CartForAuthenticatedUser(request)
        cart_info = user_cart.get_cart_info()
        total_price = cart_info['cart_total_price']
        session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': 'SHOPGRIDS product'
                        },
                        'unit_amount': int(total_price*100)
                    },
                    'quantity': 1
                }
            ],
            mode='payment',
            success_url=request.build_absolute_uri(reverse("payment_success")),
            cancel_url=request.build_absolute_uri(reverse("payment_success")),
        )

        return redirect(session.url, 303)


def payment(request):

    categories = Category.objects.all()
    working_hours = WorkingHours.objects.all()
    standard_settings = StandardSettings.objects.get()
    cart_info = get_cart_data(request)
    logo = Logo.objects.get()

    context = {
        'title': 'Checkout',
        'categories': categories,
        'working_hours': working_hours,
        'standard_settings': standard_settings,
        'order': cart_info['order'],
        'products': cart_info['products'],
        'cart_total_price': cart_info['cart_total_price'],
        'logo': logo
    }

    return render(request, 'pages/successfulpayment.html', context)


def success(request):
    user_cart = CartForAuthenticatedUser(request)
    user_cart.clear()
    messages.success(request, 'Paid successfully!')
    user_id = request.user.id

    return redirect("orders_page", user_id=user_id)
