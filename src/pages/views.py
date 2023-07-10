from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import Account
from django.contrib.auth import authenticate, login

@login_required
def homePageView(request):
    print("DO WE EVEN VISIT THE HOMEPAGEVIEW FUNCTION!????")
    accounts = Account.objects.exclude(user_id=request.user.id)
    accounts = []
    #users = User.objects.all()
    return render(request, 'pages/index.html', {'accounts': accounts})

def loginView(request):
    print("DO WE EVEN VISIT THIS?")
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            print("LoL")
    else:
        return render(request, 'pages/login.html')

@login_required
def noteWriteView(request):
    if request.method == 'POST':
        to = User.objects.get(username=request.POST.get('to'))
        noteText = int(request.POST.get('notetext'))
        request.user.account.note = noteText
        request.user.save()

    return redirect('home')