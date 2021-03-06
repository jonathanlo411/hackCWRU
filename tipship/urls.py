# Django Imports
from django.contrib import admin
from django.urls import path

# View Imports
from landing.views import landing, about
from signup.views import signup
from login.views import login
from dashboard.views import dashboard, get_data, check_user

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing, name="landing"),
    path('about', about, name="about"),
    path('signup', signup, name="signup"),
    path('login', login, name="login"),
    path('dashboard', dashboard, name="dashboard"),
    path('api/data', get_data),
    path('api/user', check_user),
]
