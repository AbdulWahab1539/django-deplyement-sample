from django.shortcuts import render
from auth_app.models import UserProfile
from django.contrib.auth.models import User
from django.forms import forms
from auth_app.forms import UserProfileForm, UserForm

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
# Create your views here.


def index(request):
    return render(request, 'auth_app/index.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def special(request):
    return HttpResponse(" YOU Have Got the Reward!!!")

def register(request):

    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_image' in request.FILES:
                profile.profile_pic = request.FILES['profile_image']

            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'auth_app/registration.html', {'user_form': user_form,
                                                          'profile_form': profile_form,
                                                          'registered': registered})
    

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user  = authenticate(username = username, password = password)
        
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            
            else:
                return HttpResponse('User is not active')
            
        else:
            print("UserName: {} Password: {}".format(username, password))
            return HttpressResponse('Invalid login credentials')
    else:
        return render(request, 'auth_app/login.html', {})
            