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
