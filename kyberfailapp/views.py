from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import Note

def loginView(request):

    return render(request, 'pages/login.html')

#@login_required
def homePageView(request):
    notes = Note.objects.exclude(user_id=request.user.id)
    return render(request, 'pages/index.html', {'notes': notes})