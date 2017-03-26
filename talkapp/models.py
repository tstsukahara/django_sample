from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    image = models.CharField(max_length=255)
    user = models.OneToOneField(User)

class Post(models.Model):
    message = models.TextField()
    image = models.CharField(max_length=255)
    user = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

class Comment(models.Model):
    message = models.TextField()
    post = models.ForeignKey(Post)
    user = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

class Group(models.Model):
    group_name = models.TextField()
    description = models.TextField()
    user = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

class Word(models.Model):
    word = models.TextField()
    group_id = models.ForeignKey(Group)
    user = models.ForeignKey(User)
    ex_word = models.TextField()
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
