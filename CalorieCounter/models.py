from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    def __str__(self):
        return f'{self.username}'
    
class BasicInfoModel(models.Model):
    Gender = [
        ('male', 'male'),
        ('female', 'female'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='user_info')
    name = models.CharField(max_length=100, null=True)
    age = models.PositiveIntegerField(null=True)
    gender = models.CharField(max_length=10, choices=Gender, null=True)
    height = models.FloatField(null=True)
    weight = models.FloatField(null=True)
    bmr = models.FloatField(null=True)

    def __str__(self):
        return f'{self.name}'

class ConsumedCalories(models.Model):
    item_name = models.CharField(max_length=100, null=True)
    calorie = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    consumed_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True , related_name='user_calorie')

    def __str__(self):
        return f'{self.consumed_by}-{self.item_name}'
    

