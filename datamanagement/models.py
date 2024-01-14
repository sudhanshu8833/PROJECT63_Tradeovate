from django.db import models
from django.db.models.fields import DateField, IntegerField
from django.contrib.auth.models import User
# Create your models here.



class Admin(models.Model):

    username=models.CharField(max_length=50,default='SOME STRING')
    email=models.EmailField(max_length=50)
    password=models.CharField(max_length=25)

    '''
    OTHER IMPORTANT INFORMATION
    '''


class orders(models.Model):
    symbol=models.CharField(max_length=20)
    time=models.DateTimeField(auto_now = True)
    price=models.FloatField(default=0)
    transaction_type=models.CharField(max_length=10)

class positions(models.Model):

    symbol=models.CharField(max_length=20,default='NA')
    time_in=models.DateTimeField(auto_now_add = True)
    price_in=models.FloatField(default=0)
    side = models.CharField(max_length=20,default='NA')
    current_price=models.FloatField(default=0)
    time_out=models.DateTimeField(default=0)
    price_out=models.FloatField(default=0)
    status=models.CharField(max_length=20,default='NA')
    token=models.CharField(max_length=20,default='NA')