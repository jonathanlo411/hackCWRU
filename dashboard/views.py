# Django Imports
from django.shortcuts import render
from django.http import JsonResponse

# Package Imports
import requests
import os
import json


# Dashboard Render
def dashboard(request):
    if (request.method=="GET") and ('code' in request.GET):

        script_dir = os.path.dirname(os.path.realpath(__file__))
        config_file = open(os.path.join(script_dir, 'config.json'))
        config = json.load(config_file)
        config_file.close()
        with open('key.txt', 'r') as file:
            data = file.readlines()
        cid = data[0].split(":")[1].replace("\n", "")
        cis = data[1].split(":")[1].replace("\n", "")

        code = request.GET['code']
        token = exchange_code(code, cid, cis)
        print(token)
    return render(request, "dashboard/dashboard.html")


# APIs
def get_data(request):
    data = {
        "day1": 2,
        "day2": 100,
        "day3": 110
    }
    return JsonResponse(data)

def post_data(request):
    if request.method=="POST":
        return JsonResponse(status=209)
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