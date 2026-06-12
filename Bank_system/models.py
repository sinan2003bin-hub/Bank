from django.db import models
from django.contrib.auth.models import User

class Bank(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    balance = models.FloatField(default=0)
    total_deposit = models.FloatField(default=0)
    total_withdraw = models.FloatField(default=0)
    deposit_count = models.IntegerField(default=0)
    withdraw_count = models.IntegerField(default=0)

