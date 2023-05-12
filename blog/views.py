import uuid
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.contrib import messages

from .models import Blog, Profile
from .helper import send_forget_password_mail

import requests

API_KEY = 'ccce2557d5234fe5848653facf389193'
URL = 'https://newsapi.org/v2/everything?q=apple&from=2023-05-10&to=2023-05-10&sortBy=popularity&apiKey=' + API_KEY


@login_required(login_url='/login')
def index(request):
    response = requests.get(URL)
    response = response.json()

    context = {
        'articles': response['articles'][:10]
    }

    return render(request, 'home.html', context)


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('l-username')
        password = request.POST.get('l-password')

        if not User.objects.filter(username=username).exists():
            messages.error(request, 'User does not exists!')
            return redirect('/login')

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return redirect('/')
        messages.error(request, 'Invalid credentials')
        return redirect('/login')

    if request.user.is_authenticated:
        return redirect('/')
    return render(request, 'login.html')


def signup_page(request):
    if request.method == 'POST':
        username = request.POST.get('s-username')
        password = request.POST.get('s-password')
        confirm_password = request.POST.get('confirm-password')
        email = request.POST.get('s-email')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('/signup')

        if User.objects.filter(email=email).exists():
            messages.success(request, 'Email is taken')
            return redirect('/signup')
        try:
            validate_password(password)
        except Exception as errors:
            for error in errors:
                messages.error(request, error)
            return redirect('/signup')

        if password != confirm_password:
            messages.error(request, 'Password does not match')
            return redirect('/signup')

        else:
            user = User.objects.create(
                username=username,
                email=email
            )
            user.set_password(password)
            user.save()

            profile_obj = Profile.objects.create(user=user)
            profile_obj.save()

            messages.success(request, 'User created successfully')

    if request.user.is_authenticated:
        return redirect('/')
    return render(request, 'signup.html')


def logout_view(request):
    logout(request)
    return redirect('/login')


@login_required(login_url='/login')
def blogs_home(request):
    user = request.user
    blogs = Blog.objects.filter(author=user)
    context = {
        'blogs': blogs
    }
    return render(request, 'blog.html', context)


@login_required(login_url='/login')
def blogs_form(request):
    if request.method == 'POST':
        user = request.user

        title = request.POST.get('title')
        content = request.POST.get('content')

        if title == '' or content == '':
            return redirect('/write_blog')

        new_blog = Blog.objects.create(
            title=title,
            content=content,
            author=User.objects.get(id=user.id)
        )

        new_blog.save()
        return redirect('/blogs')

    return render(request, 'blog_form.html')


@login_required(login_url='/login')
def delete_blog(request, pk):
    user = request.user

    blog = Blog.objects.get(id=int(pk), author=user)
    blog.delete()

    return redirect('/blogs')


def change_password(request, token):
    context = {}

    try:
        profile_obj = Profile.objects.filter(
            forget_password_token=token).first()
        context = {'user_id': profile_obj.user.id}
        print(context)

        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            user_id = request.POST.get('user_id')

            if user_id is None:
                messages.error(request, 'No user id found.')
                return redirect(f'/change_password/{token}/')

            if new_password != confirm_password:
                messages.error(request, 'Both passwords should be equal.')
                return redirect(f'/change_password/{token}/')

            user_obj = User.objects.get(id=user_id)
            user_obj.set_password(new_password)
            user_obj.save()
            messages.success(request, 'Password has been reset')
            return redirect('/login')

    except Exception as e:
        print(e)
    return render(request, 'change_password.html', context)


def forgot_password(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')

            if not User.objects.filter(username=username).first():
                messages.error(request, 'No user found with this username.')
                return redirect('/forgot_password/')

            user_obj = User.objects.get(username=username)
            token = str(uuid.uuid4())
            profile_obj = Profile.objects.get(user=user_obj)
            profile_obj.forget_password_token = token
            profile_obj.save()
            send_forget_password_mail(user_obj.email, token)
            messages.success(request, 'An email is sent.')
            return redirect('/forgot_password/')

    except Exception as e:
        print(e)
    return render(request, 'forgot_password.html')
