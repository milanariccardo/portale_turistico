from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models
from userManagement.models import Profile


# Create your models here.


# def get_deleted_user():
#     return get_user_model().objects.get_or_create(
#         username=u'deleted',
#         password=u'password',
#         profile__email='ciiio@gmial.com')[0]
#     #return g.objects.get_or_create(username='deleted')[0]


class Category(models.Model):
    title = models.CharField(max_length=30, unique=True)


class Thread(models.Model):
    # user = models.ForeignKey(Profile, on_delete=models.SET(get_deleted_user()))
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)
    text = models.TextField()
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default="None")

    def get_create_date(self):
        return self.created_at.strftime("%d/%m/%Y")

    def get_user(self):
        return self.user.user


class Comment(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    # user = models.ForeignKey(Profile, on_delete=models.SET(get_deleted_user()))
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

    def get_create_date(self):
        return self.created_at.strftime("%d/%m/%Y")

    def get_user(self):
        return self.user.user
