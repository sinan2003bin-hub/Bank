from urllib import request

from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

def home(request):

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)

            return redirect("dashboard")
        
        return render(request, "home.html", 
                {
                    "error": "Password or username is incorrect"
                }
            )
    
    return render(request, "home.html")

def signup(request):

    if request.method == "POST":

        username = request.POST["username"]
        email = request.POST["email"]

        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if password != confirm_password:

            return render(request,"signup.html",
                {
                    "error":"Passwords do not match"
                }
            )

        User.objects.create_user(
            username=username,
            password=password,
            email=email
        )

        return redirect("home")

    return render(request,"signup.html")

@login_required
def dashboard(request):
    return render(request,"dashboard.html")

