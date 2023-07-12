from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import Account, Note
from django.contrib.auth import authenticate, login

@login_required
def homePageView(request):
    account = Account.objects.get(user_id=request.user.id)
    accounts = Account.objects.exclude(user=request.user)
    doctor = account.doctor
    #users = User.objects.all()
    #account_list = list(accounts)
    #notes = [account.note for account in accounts]
    notes = Note.objects.filter(user_id=request.user.id)
    print("NOTES: " + str(notes))
    #doctorstatus = [account.doctor for account in accounts]
    print("DOCTOR: " + str(account.doctor))
    #print("ACCOUNT_LIST: " + str(account_list))
    print("ACCOUNTS: " + str(list(accounts)))
    return render(request, 'pages/index.html', {'notes': notes, 'accounts': accounts, 'doctor': doctor})

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
        toUser = User.objects.get(username=request.POST.get('to'))
        noteText = request.POST.get('notetext')
        note = Note.objects.create(user=toUser, note=noteText)
        #request.user.account.note = noteText
        #request.user.save()
        note.save()

    return redirect('home')
