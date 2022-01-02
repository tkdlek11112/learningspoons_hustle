from django.db import models


# Create your models here.
class User(models.Model):
    email = models.TextField(unique=True)
    password = models.TextField()
    nickname = models.TextField()
    name = models.TextField()
    profile_image = models.TextField()


<<<<<<< HEAD
class Doridos(models.Model):
=======
class Learningspoons(models.Model):
>>>>>>> shop
    email = models.TextField(unique=True)
    password = models.TextField()
    nickname = models.TextField()
    name = models.TextField()
    profile_image = models.TextField()

<<<<<<< HEAD
# 아무말 테스트 입력
=======
>>>>>>> shop
