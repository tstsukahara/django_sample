from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile
from .models import Post
from .forms import UserForm, UserUpdateForm, PostForm, CommentForm
from django.conf import settings
from django.contrib import messages
import time
import os

UPLOAD_DIR = settings.STATICFILES_DIRS[0] + '/images/'

def home(request):
    return render(request, 'talkapp/home.html')
    # return render(request, 'startbootstrap-sb-admin-2-gh-pages/pages/tables.html')

def user_create(request):
    return render(request, 'talkapp/user_create.html')

def user_store(request):
    form = UserForm(request.POST)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()

        profile = Profile()

        if 'file' in request.FILES:
            now = time.time()
            image_file = request.FILES['file']
            path = UPLOAD_DIR + str(now) + image_file.name
            destination = open(path, 'wb+')
            for chunk in image_file.chunks():
                destination.write(chunk)
            destination.close()
            profile.image = str(now) + image_file.name
        else:
            profile.image = "default.jpg"

        profile.user = user
        profile.save()

        user = authenticate(username=user.username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)

        return redirect('post_index')

    context = {
        "form": form,
    }
    return render(request, 'talkapp/user_create.html', context)

@login_required(login_url='/getlogin/')
def user_edit(request):
    user = request.user
    context = {
        'user' : user
    }
    return render(request, 'talkapp/user_edit.html', context)

@login_required(login_url='/getlogin/')
def user_update(request):
    form = UserUpdateForm(request.POST, instance=request.user)
    current_email = request.user.email
    if form.is_valid():
        user = form.save(commit=False)
        if form.cleaned_data['email'] != '':
            user.email = form.cleaned_data['email']
        else:
            user.email = current_email
        if form.cleaned_data['password'] != '':
            password = form.cleaned_data['password']
            user.set_password(password)

        user.save()

        if 'file' in request.FILES:
            if user.profile.image != "default.jpg":
                old_image_file = UPLOAD_DIR + user.profile.image
                os.remove(old_image_file)

            now = time.time()
            image_file = request.FILES['file']
            path = UPLOAD_DIR + str(now) + image_file.name
            destination = open(path, 'wb+')
            for chunk in image_file.chunks():
                destination.write(chunk)
            destination.close()
            user.profile.image = str(now) + image_file.name
            user.profile.save()

        if form.cleaned_data['password'] != '':
            user = authenticate(username=user.username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)

        return redirect('post_index')

    context = {
        "form": form,
    }
    return render(request, 'talkapp/user_edit.html', context)


@login_required(login_url='/getlogin/')
def post_index(request):
    word = request.GET.get("word")
    if word:
        posts = Post.objects.filter(message__contains=word).order_by('created_at').reverse()
    else:
        posts = Post.objects.all().order_by('created_at').reverse()
    context = {
        'posts' : posts
    }
    return render(request, 'talkapp/post_index.html', context)

@login_required(login_url='/getlogin/')
def post_show(request, id):
    post = Post.objects.get(id=id)
    comments = post.comment_set.all()
    context = {
        'post' : post,
        'comments' : comments
    }
    return render(request, 'talkapp/post_show.html', context)

@login_required(login_url='/getlogin/')
def post_create(request):
    return render(request, 'talkapp/post_create.html')

@login_required(login_url='/getlogin/')
def post_store(request):
    form = PostForm(request.POST)
    if form.is_valid():
        post = form.save(commit=False)
        post.user = request.user

        if 'file' in request.FILES:
            now = time.time()
            image_file = request.FILES['file']
            path = UPLOAD_DIR + str(now) + image_file.name
            destination = open(path, 'wb+')
            for chunk in image_file.chunks():
                destination.write(chunk)
            destination.close()
            post.image = str(now) + image_file.name
        else:
            post.image = "no image"

        post.save()
        return redirect('post_index')

    context = {
        "form": form,
    }
    return render(request, 'talkapp/post_create.html', context)

@login_required(login_url='/getlogin/')
def post_destroy(request, id):
    post = Post.objects.get(id=id)
    post.delete()

    return redirect('post_index')


@login_required(login_url='/getlogin/')
def comment_create(request, post_id):
    context = {
        'post_id' : post_id
    }
    return render(request, 'talkapp/comment_create.html', context)

@login_required(login_url='/getlogin/')
def comment_store(request, post_id):
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = Post.objects.get(id=post_id)
        comment.user = request.user
        comment.save()

        return redirect('post_show', id=post_id)

    context = {
        "form": form,
    }
    return render(request, 'talkapp/comment_create.html', context)


def getLogin(request):
    return render(request, 'talkapp/getlogin.html')

def postLogin(request):
    email = request.POST['email']
    password = request.POST['password']

    try:
       username = User.objects.get(email=email).username
    except User.DoesNotExist:
       username = None

    if username is not None:
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, 'You have successfully logged in')
                return redirect('post_index')

    messages.error(request, 'There was a problem with your email or password')
    return render(request, 'talkapp/getlogin.html')

def getLogout(request):
    logout(request)
    return render(request, 'talkapp/home.html')
