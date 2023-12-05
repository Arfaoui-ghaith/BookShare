from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User

from core.models import Comment


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'mb-2 bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-green-600 '
                 'focus:border-green-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 '
                 'dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
        'placeholder': 'username',
        'required': True
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'mb-2 bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-green-600 '
                 'focus:border-green-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 '
                 'dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
        'placeholder': 'password',
        'required': True
    }))


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'mb-2 bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-green-600 '
                 'focus:border-green-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 '
                 'dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
        'placeholder': 'username',
        'required': True
    }))

    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'mb-2 bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-green-600 '
                 'focus:border-green-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 '
                 'dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
        'placeholder': 'name@company.com',
        'required': True
    }))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'mb-2 bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-green-600 '
                 'focus:border-green-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 '
                 'dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
        'placeholder': '••••••••',
        'required': True
    }))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'mb-2 bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-green-600 '
                 'focus:border-green-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 '
                 'dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
        'placeholder': '••••••••',
        'required': True
    }))


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email']


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs['class'] = 'form-control'
        self.fields['new_password1'].widget.attrs['class'] = 'form-control'
        self.fields['new_password2'].widget.attrs['class'] = 'form-control'


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
