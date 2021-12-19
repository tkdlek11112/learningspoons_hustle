from django.db import models


# Create your models here.
class User(models.Model):
    email = models.TextField(unique=True)
    password = models.TextField()
    nickname = models.TextField()
    name = models.TextField()
    profile_image = models.TextField()


class Sohee(models.Model):
    email = models.TextField(unique=True)
    password = models.TextField()
    nickname = models.TextField()
    name = models.TextField()
    profile_image = models.TextField()
# 테스트 주석 추가합니다!
# 주석 한번 더 추가