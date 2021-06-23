from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserModel


class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = UserModel
        fields = ['username', 'email']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['username', 'email']
