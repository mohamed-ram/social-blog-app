from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib import messages
from blog.models import Post
from .forms import (SignUpForm, EditInfoForm,
                    LoginForm, ChangePasswordForm,
                    ResetPasswordForm, EditProfileForm)
from .models import Profile
from django.contrib.auth.decorators import login_required

# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             messages.success(request, "You have successfully logged in!")
#             return redirect('blog:posts_list')
#         else:
#             messages.error(request, "Something went wrong, try again..", extra_tags='danger')
#             return redirect('account:login')
#     return render(request, 'account/login.html', {})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['user_name'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, 'successfully logged in!')
                    return redirect('blog:dashboard')
                else:
                    messages.error(request, 'Disabled account!', extra_tags='danger')
                    return redirect('account:login')
            else:
                messages.error(request, 'Failed Login!', extra_tags='danger')
                return redirect('account:login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.success(request, 'You have successfully logged out!')
    return redirect('blog:home')


def user_register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            profile = Profile.objects.create(user=user)
            messages.success(request, "You have successfully created a new account!")
            return redirect('account:edit_profile', )
    else:
        form = SignUpForm()
    return render(request, 'account/register.html', {'form': form})


@login_required(login_url='account:login')
def user_edit_info(request):
    if request.method == 'POST':
        form = EditInfoForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "You have successfully edited your info!")
            return redirect('blog:home')
    else:
        form = EditInfoForm(instance=request.user)
    return render(request, 'account/edit_info.html', {'form': form})


def user_profile(request, user_name):
    user = User.objects.get(username=user_name)
    posts = Post.objects.filter(author__username=user_name)
    return render(request, 'account/profile.html', {'user': user, 'posts': posts})


@login_required(login_url='account:login')
def user_edit_profile(request):
    form = EditProfileForm(instance=request.user.profile)
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            us = form.save(commit=False)
            us.user = request.user
            us.save()
            messages.success(request, 'Profile Info edited successfully')
            return redirect('blog:dashboard')
        else:
            messages.error(request, 'Error, Something went wrong!')
    return render(request, 'account/edit_profile.html', {'form': form})


@login_required(login_url='account:login')
def user_change_password(request):
    form = ChangePasswordForm(request.user)
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "You have successfully edited your password!")
            return redirect('blog:dashboard')
        else:
            messages.error(request, "Something went wrong!", extra_tags='danger')
    return render(request, 'account/change_password.html', {'form': form})


@login_required(login_url='account:login')
def user_reset_password(request):
    form = ResetPasswordForm()
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            if function_checkemail(email):
                form.save(from_email='mo74m6d@gmail.com', email_template_name='account/email_template.html')
                return redirect('account:login')
    return render(request, 'account/reset_password.html', {'form': form})


def toggle_follow(request, user_name):
    toggle_user = User.objects.get(username__exact=user_name)
    user_profile = Profile.objects.get(user=request.user)
    if toggle_user in user_profile.following.all():
        user_profile.following.remove(toggle_user)
    else:
        user_profile.following.add(toggle_user)
    return redirect('account:profile', user_name=toggle_user.username)