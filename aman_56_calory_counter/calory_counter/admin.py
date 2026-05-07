from django.contrib import admin
from calory_counter.models import *

# Register your models here.
admin.site.register([User, CaloryModel, BasicInfoModel])

