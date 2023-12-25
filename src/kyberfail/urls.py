from django.urls import path, include

from .views import homePageView, loginView, registerView, patientsView, notesView, noteView, profileView, searchView

urlpatterns = [
    path('', homePageView, name='home'),
    path('login/', loginView, name='login'),
    path('register/', registerView, name='registerView'),
    path('patients/', patientsView, name='patients'),
    path('notes/', notesView, name='notes'),
    path('note/', noteView, name='note'),
    path('profile/', profileView, name='profile'),
    path('search/', searchView, name='search')
]