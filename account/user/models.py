from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
import random
import string


class User(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    birthdate = models.DateField()
    nationality = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    re_password = models.CharField(max_length=100)

    def __str__(self):
        return self.firstname


class UserToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100)

    def __str__(self):
        return self.token


class UserQuestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.TextField(max_length=500, null=True, blank=True)
    answer = models.TextField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.question


@receiver(post_save, sender=User)
def create_user_token(sender, instance, **kwargs):
    if not UserToken.objects.filter(user=instance).exists():
        chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
        token = ''.join(random.choices(chars, k=30))
        UserToken.objects.create(
            user=instance,
            token=token
        )
