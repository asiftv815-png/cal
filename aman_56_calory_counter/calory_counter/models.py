from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    
    def __str__(self):
        return f'{self.username}'
    
    
class BasicInfoModel(models.Model):
    GENDER_CHOICES = (
    ('male', 'Male'),
    ('female', 'Female'),
    )
    username = models.OneToOneField(User , on_delete=models.CASCADE, null=True, related_name='user_info')
    name = models.CharField(max_length=100, null=True)
    age = models.IntegerField(null=True)
    gender = models.CharField(max_length=20,null=True, choices = GENDER_CHOICES)
    height = models.FloatField(null=True)
    weight = models.FloatField(null = True)
    bmr = models.FloatField(null=True)
    
    def __str__(self):
        return f'{self.username}'
    

class CaloryModel(models.Model):
    food = models.CharField(max_length=100, null=True)
    consume_calory = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    consumed_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='user_calory')
    
    def __str__(self):
        return f'{self.consumed_by.username}'
    
