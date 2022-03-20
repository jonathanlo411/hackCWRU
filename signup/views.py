from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login

# User Creation
from .models import userprofile
from .forms import UserCreation

# Create your views here.
def signup(request):
    if request.method == 'POST':
        user_form = UserCreation(data=request.POST)
        if user_form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            if User.objects.filter(username = username).exists():
                return render(request,'signup/signup_error.html', {"ucreation": UserCreation, "error": "Username Already Exists!"})
            else:
                # saving user for login info
                user = User.objects.create_user(username=username, password=password)
                user.set_password(password)
                user.save()
                # creating a userprofile
                userp = userprofile(username = username, password = password)
                userp.save()
                u = User.objects.get(username = username)
                user = authenticate(username=u.get_username(),password=password)
                login(request, user)
                return HttpResponseRedirect('/dashboard')

    context = {
        "ucreation": UserCreation
    }
    return render(request, 'signup/signup.html', context)
