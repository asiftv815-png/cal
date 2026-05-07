from django.shortcuts import render, redirect
from django.contrib.auth import login,logout
from datetime import date
from calory_counter.models import * 
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from calory_counter.form import *
from django.db.models import Sum,Count

def reg_page(r):
    if r.method == 'POST':
        form_data = RegUser(r.POST)
        if form_data.is_valid():
            form_data.save()
            return redirect('login_page')
    else:
        form_data = RegUser()
    context = {
        "form_data": form_data,
        "form_title": "REG USER",
        "form_btn": "REG BAIT",
    }
    return render(r, 'master/basef.html', context)


def login_page(r):
    if r.method == 'POST':
        form_data = LoginUser(r, data=r.POST)
        if form_data.is_valid():
            user = form_data.get_user()
            login(r, user)
            return redirect('home_page')
    form_data = LoginUser()
    context = {
        "form_data": form_data,
        "form_title": "log USER",
        "form_btn": "log BAIT",
    }
    return render(r, 'master/basef.html', context)


@login_required
def home_page(request):
    try:
        current_user = request.user
        bmr = round(request.user.user_info.bmr, 2)
    except:
        bmr = 0

    today = date.today()
    today_consumed_data= CaloryModel.objects.filter(
        consumed_by = current_user,
        created_at = today
    )
    total_consumed_data = CaloryModel.objects.aggregate(
        total_calorie=Sum('consume_calory'),
        total_count = Count('consume_calory'),
    
    )
    total_cal = total_consumed_data['total_count']
    less_more = bmr - total_cal

    if bmr > total_cal:
        suggestion = 'Eat more'
    else:
        suggestion = 'Eat less'





    context={
        'required_calorie' : bmr,
        'today_consumed_data' : today_consumed_data,
        'total_count' : total_consumed_data['total_count'],
        'consumed_calories' : total_cal,
        'less_more' : less_more,
        'suggestion' : suggestion
    }

    return render(request, 'dasb.html', context)
@login_required

def logout_page(request):
    logout(request)
    messages.success(request, 'Logout Successfully')
    return redirect('login_page')

@login_required
def profile_page(request):

    return render(request, 'profile.html')

@login_required
def update_page(request):
    try:
        current_user = request.user.user_info
    except:
        current_user = None

    if request.method == 'POST':
        form_data = ProfileUpdateFrom(request.POST, instance=current_user)
        #using commit false as we are excluded 2 fields 
        # but we need to access the database
        if form_data.is_valid():
            data = form_data.save(commit=False)
            data.user = request.user
            weight = data.weight
            height = data.height
            age = data.age
            if data.gender == 'Male':
                bmr = 66.47+(13.75 * weight) + (5.003 * height) - (6.775 *age)
                #BMR= 66.47+(13.75 x weight in kg) + (5.003 x height in cm) - (6.755 x age in years)
            else:
                bmr = 655.1+(9.563 * weight) + (1.850 * height) - (4.676 *age)
                # BMR=655.1+(9.563 x weight in kg)+(1.850 xheight in cm) - (4.676 x age in years)
            data.bmr = bmr
            data.save()
            return redirect('profile_page')

    form_data = ProfileUpdateFrom(instance=current_user)
    context={
        'form_data' : form_data,
        'form_name' : 'Update Profile Info',
        'form_btn' : 'Update'
    }

    return render(request, 'master/basef.html', context)

def consumed_calories(request):
    consumed_data = CaloryModel.objects.filter(consumed_by = request.user)
    context = {
        'consumed_data': consumed_data
    }

    return render(request, 'cal_list.html', context)

def add_calorie(request):
    if request.method == 'POST':
        form_data = ConsumedCaloireForm(request.POST)
        if form_data.is_valid():
            data = form_data.save(commit=False)
            data.consumed_by = request.user
            data.save()
            
            return redirect('consumed_calories')

    form_data = ConsumedCaloireForm()
    context={
        'form_data' : form_data,
        'form_name' : 'Add Calorie Info',
        'form_btn' : 'Add Calorie'
    }
    return render(request, 'master/basef.html', context)

def edit_calorie(request, id):
    try:
        data = CaloryModel.objects.get(id=id)
    except:
        data = None
    if request.method == 'POST':
        form_data = ConsumedCaloireForm(request.POST, instance=data)
        if form_data.is_valid():
            data = form_data.save(commit=False)
            data.consumed_by = request.user
            data.save()
            
            return redirect('consumed_calories')

    form_data = ConsumedCaloireForm(instance=data)
    context={
        'form_data' : form_data,
        'form_name' : 'Edit Calorie Info',
        'form_btn' : 'Update Calorie'
    }
    return render(request, 'master/basef.html', context)

def delete_calorie(request, id):
    try:
        data = CaloryModel.objects.get(id=id)
    except:
        data = None
    data.delete()
   
    return redirect('consumed_calories')
