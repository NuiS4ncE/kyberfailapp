from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import Account, Note
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from django.db.models import Q

@login_required
def homePageView(request):
    account = Account.objects.get(user_id=request.user.id)
    accounts = Account.objects.exclude(user=request.user)
    doctor = account.doctor
    notes = Note.objects.filter(user_id=request.user.id)
    superuser = account.user.is_superuser

    return render(request, 'pages/index.html', {'notes': notes, 'accounts': accounts, 'doctor': doctor, 'superuser': superuser})

def loginView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            print("Invalid login credentials")
            return HttpResponse("Invalid login credentials")       
    else:
        return render(request, 'pages/login.html')
    
def registerView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        firstName = request.POST['firstName']
        lastName = request.POST['lastName']
        try:
            user = User.objects.create_user(username=username, email=email, password=password, first_name=firstName, last_name=lastName)
        except IntegrityError as e:
                # Security misconfiguration
                #error = "Registration failed. More info: " + str(e.args[0])
                #print(error)
                error = "Registration failed."
                print(str(e))
                return HttpResponse(error)
        user.save()
        account = Account.objects.create(user=user, doctor=False)
        account.save()
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'pages/register.html')

@login_required
def noteView(request, noteId):
    # Broken access control here
    note = Note.objects.get(id=noteId)
    account = Account.objects.get(user_id=request.user.id)
    doctor = account.doctor
    superuser = account.user.is_superuser
    if (note.user_id is not request.user.id and not doctor):
        return redirect('home')

    return render(request, 'pages/note.html', {'note': note, 'doctor': doctor, 'superuser': superuser})

@login_required
def patientView(request, patientId):
    account = Account.objects.get(user_id=request.user.id)
    doctor = account.doctor
    superuser = account.user.is_superuser
    if doctor == False:
        return redirect('home')
    patient = User.objects.get(id=patientId)

    return render(request, 'pages/patient.html', {'patient': patient, 'doctor': doctor, 'superuser': superuser})


@login_required
def notesView(request):
    account = Account.objects.get(user_id=request.user.id)
    accounts = Account.objects.exclude(user=request.user).exclude(user__is_superuser=True)
    doctor = account.doctor
    superuser = account.user.is_superuser

    if doctor == True:
        notes = Note.objects.all()
    else:
        return redirect('home')
    
    if request.method == 'POST':
        if 'noteId' in request.POST:
            try:
                note = Note.objects.get(id=request.POST.get('noteId'))
                note.delete()
            except Note.DoesNotExist:
                error = "Something went wrong. More info: " + str(Note.DoesNotExist)
                print(error)
                return HttpResponse(error)
            return redirect('notes')
        else: 
            try: 
                toUser = User.objects.get(username=request.POST.get('to'))
                noteTitle = request.POST.get('title')
                noteDescription = request.POST.get('description')
                note = Note.objects.create(user=toUser, title=noteTitle, description=noteDescription)
                note.save()
            except User.DoesNotExist:
                error = "Something went wrong. More info: " + str(User.DoesNotExist)
                print(error)
                return HttpResponse(error)
            return redirect('notes')    
    return render(request, 'pages/notes.html', {'notes': notes, 'accounts': accounts, 'doctor': doctor, 'superuser': superuser})

@login_required
def patientsView(request):
    accounts = Account.objects.exclude(user=request.user).exclude(user__is_superuser=True)
    account = Account.objects.get(user_id=request.user.id)
    doctor = account.doctor
    superuser = account.user.is_superuser
    if doctor == False:
        return redirect('home')
    return render(request, 'pages/patients.html', {'accounts': accounts, 'doctor': doctor, 'superuser': superuser})

@login_required
def profileView(request):
    account = Account.objects.get(user_id=request.user.id)
    doctor = account.doctor
    superuser = account.user.is_superuser

    return render(request, 'pages/profile.html', {'doctor': doctor, 'superuser': superuser})

@login_required
def searchView(request):
    # Injection here
    account = Account.objects.get(user_id=request.user.id)
    query = request.GET.get('query')
    doctor = account.doctor
    superuser = account.user.is_superuser
    if query is not None:
        if doctor == True or superuser == True:
            noteResults = Note.objects.filter(Q(title__icontains=query) | Q(description__icontains=query)).distinct()
        else:
            noteResults = Note.objects.filter(Q(user=request.user),
                Q(title__icontains=query) | Q(description__icontains=query)).distinct()
        
        return render(request, 'pages/search.html', {'noteResults': noteResults, 'query': query, 'doctor': doctor, 'superuser': superuser})
    else:
        return redirect('notes')
    
@login_required
def adminView(request):
    account = Account.objects.get(user_id=request.user.id)
    doctor = account.doctor
    superuser = account.user.is_superuser
    if superuser == False:
        return redirect('home')
    return render(request, 'pages/admin.html', {'doctor': doctor, 'superuser': superuser})