from django.db import models


# Create your models here.
class Feed(models.Model):
    content = models.TextField()
    image = models.TextField()
    profile_image = models.TextField()
    nickname = models.TextField()


class Reply(models.Model):
    feed_id = models.IntegerField()
    nickname = models.TextField()
    content = models.TextField()


class Like(models.Model):
    feed_id = models.IntegerField()
    email = models.TextField()

    class Meta:
        unique_together = ('feed_id', 'email',)


class Product(models.Model):
    image = models.TextField()
    seller = models.TextField()
    description = models.TextField()
    price = models.IntegerField()
    name = models.TextField(default='')


class Cart(models.Model):
    email = models.TextField()
    product_id = models.IntegerField()
    count = models.IntegerField()

    class Meta:
        unique_together = ('email', 'product_id')

class Review(models.Model):
    review = models.TextField()
    nickname = models.TextField()


class ProductReview(models.Model):
    review = models.TextField()
    nickname = models.TextField()
    product_id = models.IntegerField()
    star = models.IntegerField(default=0)


class FavoriteProducts(models.Model):
    product_id = models.IntegerField()
    email = models.TextField()

    class Meta:
        unique_together = ('email', 'product_id')