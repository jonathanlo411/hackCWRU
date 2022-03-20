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
                return HttpResponseRedirect('https://discord.com/api/oauth2/authorize?client_id=954815661174055002&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Fdashboard&response_type=code&scope=identify%20email')

    context = {
        "ucreation": UserCreation
    }
    return render(request, 'signup/signup.html', context)
