from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import Account, Note
from django.contrib.auth import authenticate, login
from django.db import IntegrityError

@login_required
def homePageView(request):
    account = Account.objects.get(user_id=request.user.id)
    accounts = Account.objects.exclude(user=request.user)
    doctor = account.doctor
    notes = Note.objects.filter(user_id=request.user.id)
    print("NOTES: " + str(notes))
    print("DOCTOR: " + str(account.doctor))
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
    
def registerView(request):
    print("REGISTERVIEW CALLED")
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        firstName = request.POST['firstName']
        lastName = request.POST['lastName']
        try:
            user = User.objects.create_user(username=username, email=email, password=password, first_name=firstName, last_name=lastName)
        except IntegrityError as e:
                error = "Registration failed. User already exists. More info: " + e.args[0]
                return HttpResponse("Something went wrong. " + error)
        user.save()
        print("CREATED USER")
        account = Account.objects.create(user=user, doctor=False)
        account.save()
        print("CREATED ACCOUNT")        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            print("LOGIN SUCCESSFUL AFTER REGISTER")
            return redirect('home')
    return render(request, 'pages/register.html')

@login_required
def noteWriteView(request):
    if request.method == 'POST':
        toUser = User.objects.get(username=request.POST.get('to'))
        noteTitle = request.POST.get('title')
        noteDescription = request.POST.get('description')
        note = Note.objects.create(user=toUser, title=noteTitle, description=noteDescription)
        note.save()

@login_required
def noteView(request):
    return render(request, 'pages/note.html')

    return redirect('home')

@login_required
def notesView(request):
    account = Account.objects.get(user_id=request.user.id)
    accounts = Account.objects.exclude(user=request.user)
    doctor = account.doctor
    notes = Note.objects.all()
    if request.method == 'POST':
        toUser = User.objects.get(username=request.POST.get('to'))
        noteTitle = request.POST.get('title')
        noteDescription = request.POST.get('description')
        note = Note.objects.create(user=toUser, title=noteTitle, description=noteDescription)
        note.save()    
    return render(request, 'pages/notes.html', {'notes': notes, 'accounts': accounts, 'doctor': doctor})

@login_required
def patientsView(request):
    accounts = Account.objects.exclude(user=request.user)
    account = Account.objects.get(user_id=request.user.id)
    doctor = account.doctor
    return render(request, 'pages/patients.html', {'accounts': accounts, 'doctor': doctor})

@login_required
def profileView(request):

    return render(request, 'pages/profile.html')