from django.urls import path
from CalorieCounter.views import *

urlpatterns = [
    path('', register_page, name='register_page'),
    path('login/', login_page, name='login_page'),
    path('logout/', logout_page, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('profile/', profile_page, name='profile_page'),
    path('update_profile/',update_profile,name='update_profile'),
     path('consumed_calorie_list/',consumed_calory_list,name='consumed_calory_list'),
    path('add_calorie/',add_calorie,name='add_calorie'),
    path('update_calorie/<int:id>/',update_calory,name='update_calory'),
    path('delete_calorie/<int:id>/',delete_calory,name='delete_calory'),
]