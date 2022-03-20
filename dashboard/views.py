# Django Imports
from urllib import response
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth import authenticate, login

# Models
from signup.models import userprofile

# Package Imports
import requests
import os
import json


# Dashboard Render
def dashboard(request):
    user = userprofile.objects.get(username = request.user)
    if (request.method=="GET") and ('code' in request.GET):

        # Grab Discord Client ID and Client Secret
        script_dir = os.path.dirname(os.path.realpath(__file__))
        config_file = open(os.path.join(script_dir, 'config.json'))
        config = json.load(config_file)
        config_file.close()
        cid = config['Discord Client ID']
        cis = config['Discord Client Secret']

        # Grab returned code from users auth
        code = request.GET['code']
        token = exchange_code(code, cid, cis)
        user_obj = get_user(token)
        
        # Updating user
        user.add(token['access_token'], token['refresh_token'])
        

    context = {
        "user": user
    }
    return render(request, "dashboard/dashboard.html", context)


# APIs
def get_data(request):
    labels = ["Thu, Fri, Sat, Sun"]
    payments = [40, 70, 40, 100]
    data = {
        "labels": labels,
        "data": payments
    }
    return JsonResponse(data)

def check_user(request):
    if request.method=="GET":
        pot_user = request.GET['user']
        if User.objects.filter(username = pot_user).exists():
            return JsonResponse({"user_exists": True}, status=200)
        return JsonResponse({"user_exists": False}, status=200)
    return JsonResponse({'error':'something bad'},status=400)


# Helper Functions
def exchange_code(code, client_id, client_secret):
    """ Exchanges Auth code for user token
    """
    url = 'https://discord.com/api/v8'
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': 'http://127.0.0.1:8000/dashboard'
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    r = requests.post('%s/oauth2/token' % url, data=data, headers=headers)
    r.raise_for_status()
    return r.json()

def get_user(token):
    url = "https://discord.com/api/v8"
    auth = token['access_token']
    headers = {
        "Authorization": f"Bearer {auth}"
    }
    r = requests.get('%s/users/@me' % url, headers=headers)
    r.raise_for_status()
    return r.json()
