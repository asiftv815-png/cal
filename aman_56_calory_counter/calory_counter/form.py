from django import forms
from calory_counter.models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class RegUser(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginUser(AuthenticationForm):
    pass

class ProfileUpdateFrom(forms.ModelForm):
    class Meta:
        model = BasicInfoModel
        fields = '__all__'
        exclude = ['user' , 'bmr']

class ConsumedCaloireForm(forms.ModelForm):
    class Meta:
        model = CaloryModel
        fields = '__all__'
        exclude = ['consumed_by']