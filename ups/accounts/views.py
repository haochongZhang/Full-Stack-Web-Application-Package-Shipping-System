from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def signup(request):
    if request.method == "POST":
        if request.POST["password1"] != request.POST["password2"]:
            return render(request, "accounts/signup.html", {"message": "please enter the same password"})
        if ',' in request.POST["username"]:
            return render(request, "accounts/signup.html", {"message": "please donot contain comma in your username"})
        else:
            try:
                User.objects.get(username=request.POST["username"])
                return render(request, "accounts/signup.html",
                              {"message": "username has already been taken, try another one"})
            except User.DoesNotExist:
                user = User.objects.create_user(request.POST["username"], password=request.POST["password1"],
                                                email=request.POST["e_mail"])
                login(request, user)
                return render(request, "accounts/login.html")
    else:
        return render(request, "accounts/signup.html")


def Login(request):
    if request.method == "POST":
        user = authenticate(username=request.POST["username"], password=request.POST["password"])
        if user is not None:
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST["next"])
            return redirect("/delivery/overviewShipment")
        else:
            return render(request, "accounts/login.html", {"message": "user or password incorrect"})
    else:
        return render(request, "accounts/login.html")


def Logout(request):
    if request.method == "POST":
        logout(request)
        return render(request, "accounts/login.html")

