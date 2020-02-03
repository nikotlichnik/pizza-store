from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=128)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'password1', 'password2']
