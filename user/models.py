from django.db import models


# Create your models here.
class User(models.Model):
    email = models.TextField(unique=True)
    password = models.TextField()
    nickname = models.TextField()
    name = models.TextField()
    profile_image = models.TextField()


class Address(models.Model):

    email = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField(blank=True, null=True)
    primary_address = models.BooleanField(default=False)


class Learningspoons(models.Model):
    email = models.TextField(unique=True)
    password = models.TextField()
    nickname = models.TextField()
    name = models.TextField()
    profile_image = models.TextField()

# 아무말쓰기
