from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserModel


class UserRegisterForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = UserModel
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.Form):
    update_value = forms.CharField(max_length=255)
