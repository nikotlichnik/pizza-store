from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegisterForm


def signup(request):
    signup_error = ''
    if request.POST:
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect(reverse('loginsys_app:login'))

    context = {
        'signup_error': signup_error,
        'form': UserRegisterForm
    }

    return render(request, 'loginsys_app/signup.html', context)


def user_login(request):
    login_error = ''

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse('pizza_store_app:catalog'))
        else:
            login_error = 'User not found :('

    context = {
        'login_error': login_error,
        'user': request.user
    }

    return render(request, 'loginsys_app/login.html', context)


def user_logout(request):
    logout(request)
    return redirect(reverse('pizza_store_app:catalog'))
