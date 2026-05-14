from django.shortcuts import render , redirect
from CalorieCounter.models import *
from CalorieCounter.forms import *
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import date
from django.db.models import Sum, Count

# Create your views here.
def register_page(request):
    if request.method == 'POST':
        form_data = RegistrationForm(request.POST)
        if form_data.is_valid():
            form_data.save()
            messages.success(request, 'Registration Successful')
            return redirect('login_page')
    form_data = RegistrationForm()
    context = {
        'form_data' : form_data,
        'form_title' : 'registration Form',
        'form_btn' : 'register',
    }
    return render(request, 'master/base_form.html', context)

def login_page(request):
    if request.method == 'POST':
        form_data = LoginForm(request, request.POST)
        if form_data.is_valid():
            user = form_data.get_user()
            login(request, user)
            messages.success(request, 'Login Successful')
            return redirect('dashboard')
    form_data = LoginForm()
    context = {
        'form_data' : form_data,
        'form_title' : 'login form',
        'form_btn' : 'Login', 
    }
    return render(request, 'master/base_form.html', context)

@login_required
def logout_page(request):
    logout(request)
    messages.success(request, 'Logout Successfully')
    return redirect('login_page')


@login_required
def dashboard(request):

    current_user = request.user

    try:
        bmr = round(request.user.user_info.bmr, 2)
    except AttributeError:
        bmr = 0

    today = date.today()

    today_consumed_data = ConsumedCalories.objects.filter(
        consumed_by=current_user,
        created_at__date=today
    )

    total_consumed_calories = today_consumed_data.aggregate(
        total_calorie=Sum('calorie'),
        total_count=Count('calorie')
    )

    total_calorie = total_consumed_calories['total_calorie'] or 0

    less_more = bmr - total_calorie

    if bmr > total_calorie:
        suggestion = 'Eat more'
    elif bmr < total_calorie:
        suggestion = 'Eat less'
    else:
        suggestion = 'Perfect intake'

    context = {
        'required_calories': bmr,
        'today_consumed_data': today_consumed_data,
        'consumed_calories': total_calorie,
        'total_count': total_consumed_calories['total_count'] or 0,
        'less_more': less_more,
        'suggestion': suggestion,
    }

    return render(request, 'dashboard.html', context)


@login_required
def profile_page(request):
   

    return render(request, 'profile.html')


@login_required
def update_profile(request):
    try:
        current_user = request.user.user_info
    except:
        current_user = None
    if request.method == 'POST':
        form_data = ProfileUpdateForm(request.POST, instance= current_user)
        if form_data.is_valid():
            data = form_data.save(commit=False)
            data.user = request.user

            weight = data.weight
            height = data.height
            age = data.age 
            if data.gender == 'male':
                bmr_calculate = 66.47 + (13.75 * weight) + (5.003 * height) - (6.755 * age)
            else:
                bmr_calculate = 655.1 + (9.563 * weight) + (1.850 * height) - (4.676 * age)
            
            data.bmr = bmr_calculate
            data.save()
            messages.success(request, "Profile Updated")
            return redirect('profile_page')
        
    form_data = ProfileUpdateForm(instance=current_user)
    context = {
        'form_data' : form_data,
        'form_title' : 'Profile update form',
        'form_btn' : 'Update',
    } 
    return render(request, 'master/base_form.html', context)



@login_required
def add_calorie(request):

    if request.method == 'POST':
        form_data = ConsumedCalorieForm(request.POST)

        if form_data.is_valid():
            data = form_data.save(commit=False)
            data.consumed_by = request.user
            data.save()

            messages.success(request, 'Calorie added')
            return redirect('consumed_calory_list')

    else:
        form_data = ConsumedCalorieForm()

    context = {
        'form_data': form_data,
        'form_title': 'Add calorie form',
        'form_btn': 'Add calorie',
    }

    return render(request, 'master/base_form.html', context)
    

    
@login_required
def consumed_calory_list(request):
    consumed_data = ConsumedCalories.objects.filter(consumed_by=request.user)
    context = {
        'consumed_data' : consumed_data
    }

    return render(request, 'calory_list.html', context)




@login_required
def update_calory(request, id):

    try:
        data = ConsumedCalories.objects.get(
            id=id,
            consumed_by=request.user
        )
    except ConsumedCalories.DoesNotExist:
        messages.error(request, 'Data not found')
        return redirect('consumed_calory_list')

    if request.method == 'POST':
        form_data = ConsumedCalorieForm(request.POST, instance=data)

        if form_data.is_valid():
            data = form_data.save(commit=False)
            data.consumed_by = request.user
            data.save()

            messages.success(request, "Update successful")
            return redirect('consumed_calory_list')

    else:
        form_data = ConsumedCalorieForm(instance=data)

    context = {
        'form_data': form_data,
        'form_title': "Update Calorie Info",
        'form_btn': 'Update Calorie'
    }

    return render(request, 'master/base_form.html', context)




@login_required
def delete_calory(request, id):

    try:
        data = ConsumedCalories.objects.get(
            id=id,
            consumed_by=request.user
        )

        data.delete()
        messages.success(request, 'Deleted successfully')

    except ConsumedCalories.DoesNotExist:
        messages.error(request, 'Data not found')

    return redirect('consumed_calory_list')