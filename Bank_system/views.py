from django.shortcuts import render, redirect
from .models import Bank
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def home(request):

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(
            request,
            username=username,
            password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")

        return render(request,"home.html",
        {
            "error":
            "Password or username is incorrect"
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
                "error":
                "Passwords do not match"
            }
                )

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email)

        Bank.objects.create(user=user,balance=0)

        return redirect("home")

    return render(request, "signup.html")


@login_required
def dashboard(request):

    bank, created = Bank.objects.get_or_create(
    user=request.user,
    defaults={"balance": 0}
    )


    action = None

    if request.method == "POST":

        action = request.POST.get("action")

        if action == "deposit" and "amount" in request.POST:

            amount = float(request.POST["amount"])

            bank.balance += amount
            bank.total_deposit += amount
            bank.deposit_count += 1

            bank.save()

        elif action == "withdraw" and "amount" in request.POST:

            amount = float(request.POST["amount"])

            if amount <= bank.balance:

                bank.balance -= amount
                bank.total_withdraw += amount
                bank.withdraw_count += 1

                bank.save()

    return render(request,"dashboard.html",
        {
            "bank": bank,
            "action": action
        }
            )


def logout_page(request):
    logout(request)

    return redirect("home")
