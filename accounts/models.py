from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver

from bank import settings


class Profile(models.Model):
    user = models.OneToOneField(User, default=0, on_delete=models.CASCADE)
    balance = models.IntegerField(default=5000)

    # def __str__(self):
      # profile = self.balance
      #  return "%s" % (self.user.username)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class Transaction(models.Model):
    sender = models.ForeignKey(Profile, related_name='sent_money', on_delete=models.CASCADE)
    receiver = models.CharField(default=0, max_length=250)
    amount = models.IntegerField(default=0)
