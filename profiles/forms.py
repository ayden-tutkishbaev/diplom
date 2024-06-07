from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
# from market.models import
from django.utils.translation import gettext_lazy as _
from market.models import Message
from market.models import Checkout
from profiles.models import Comment, Profile
from profiles.utils import phone_number_validation


class RegisterForm(UserCreationForm):
    username = forms.CharField(label='Username', max_length=20, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                              'placeholder': 'Username'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control',
                                                                           'placeholder': 'email'}))
    password1 = forms.CharField(label='Password', max_length=20,
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'placeholder': 'Password'}))
    password2 = forms.CharField(label='Password', max_length=20,
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'placeholder': 'Confirm password'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username', max_length=20, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                              'placeholder': 'Username'}))
    password = forms.CharField(label='Password', max_length=20,
                               widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'placeholder': 'Password'}))


class CheckoutForm(forms.ModelForm):

    class Meta:
        model = Checkout
        fields = ('name',
                  'phone_number',
                  'email',
                  'address',
                  'city',
                  'country',
                  'payment_method',
                  )

    PAYMENT_METHOD = (
        ('credit_card', _('Credit card')),
    )

    widgets = {
        'name': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Name'
        }),

        'phone_number': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Phone number'
        }),

        'email': forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email'
        }),
        'payment_method': forms.Select(
            choices=PAYMENT_METHOD,
            attrs={'class': 'form-control',
        }),
        'address': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Address"
        }),
        'city': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "City"
        }),
        'country': forms.TextInput(attrs={
             'class': 'form-control',
             'placeholder': "Country"
        })
    }


class UserForm(forms.ModelForm):
    username = forms.CharField(label='Username', max_length=20, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                              'placeholder': 'Username'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control',
                                                                           'placeholder': 'email'}))

    class Meta:
        model = User
        fields = (
            'username', 'email'
        )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'name', 'location', 'phone_number'
        )

    widgets = {
        'name': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your name'
        }),
        'location': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your location'
        }),
        'phone_number': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your phone number'
        })
    }


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = (
            'phone_number', 'text',
        )

    widgets = {
        'phone_number': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Phone number'
        }),
        'text': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Text'
        })
    }


class CommentForm(forms.ModelForm):
    RATING = (
        ('five', _('5')),
        ('four', _('4')),
        ('three', _('3')),
        ('two', _('2')),
        ('one', _('1')),
        ('zero', _('0'))
    )

    class Meta:
        model = Comment
        fields = (
            'text',
            'rating'
        )

    widgets = {
        'text': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your comment'
        }),
        'rating': forms.Select(attrs={
            'class': 'form-control',
        }, choices=RATING)
    }

    # name = forms.CharField(label='Name', max_length=250, widget=forms.TextInput(attrs={'class': 'form-control',
    #                                                                                    'placeholder': 'Name'}))
    # phone_number = forms.IntegerField(label='Phone', widget=forms.TextInput(attrs={'class': 'form-control',
    #                                                                         'placeholder': 'Phone number'}))
    # customer_email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control',
    #                                                                        'placeholder': 'email'}))
    # payment_method = forms.ChoiceField(label='Payment Method', choices=PAYMENT_METHOD,
    #                                     widget=forms.Select(attrs={'class': 'form-control'}))
    # address = forms.CharField(label='Address', max_length=250,
    #                           widget=forms.TextInput(attrs={'class': 'form-control',
    #                                                         'placeholder': "Address"}))
    # city = forms.CharField(label='City', max_length=250,
    #                        widget=forms.TextInput(attrs={'class': 'form-control',
    #                                                      'placeholder': "City"}))
    # country = forms.CharField(label='Country', max_length=250,
    #                           widget=)




