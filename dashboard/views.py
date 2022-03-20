from telnetlib import STATUS
from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def dashboard(request):
    return render(request, "dashboard/dashboard.html")


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