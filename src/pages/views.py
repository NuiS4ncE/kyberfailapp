from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import Account
from django.contrib.auth import authenticate, login

@login_required
def homePageView(request):
    accounts = Account.objects.exclude(user_id=request.user.id)
    #users = User.objects.all()
    return render(request, 'pages/index.html', {'accounts': accounts})

def loginView(request):
    if request.method == 'POST':
        username = request.POST['username']
        #print("THIS IS THE USERNAME: " + username)
        password = request.POST['password']
        #print("THIS IS THE PASSWORD: " + password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print("LOGIN SUCCESSFUL, REDIRECTING")
            return redirect('home')
        else:
            print("LoL")
    else:
        print("RENDERING LOGIN PAGE AGAIN")
        return render(request, 'pages/login.html')

@login_required
def noteWriteView(request):
    if request.method == 'POST':
        to = User.objects.get(username=request.POST.get('to'))
        noteText = int(request.POST.get('notetext'))
        request.user.account.note = noteText
        request.user.save()

    return redirect('home')