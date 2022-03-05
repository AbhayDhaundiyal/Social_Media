from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser

class User(AbstractBaseUser):
    email = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)
    user_id  = models.AutoField(primary_key=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    def __str__(self):
        return self.email

class post(models.Model):
    desc = models.TextField(max_length=20, default='none')
    title = models.TextField(max_length=320)
    post_id = models.AutoField(primary_key=True)
    created_on = models.DateField(default=timezone.now)
    likes = models.IntegerField(default=0)
    unlikes = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.title

class comments(models.Model):
    text = models.TextField(max_length=200)
    post = models.ForeignKey(post, on_delete=models.CASCADE)
    by = models.CharField(max_length=200, default="xx")
    def __str__(self):
        return self.text

class following(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE)
    followed = models.CharField(max_length=200)
    def __str__(self):
        return self.followed
