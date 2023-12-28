from django.urls import path, include

from .views import homePageView, loginView, registerView, patientsView, notesView, noteView, profileView, searchView, patientView, adminView

urlpatterns = [
    path('', homePageView, name='home'),
    path('login/', loginView, name='login'),
    path('register/', registerView, name='registerView'),
    path('patients/', patientsView, name='patients'),
    path('notes/', notesView, name='notes'),
    path('note/<int:noteId>', noteView, name='note'),
    path('patient/<int:patientId>', patientView, name='patient'),
    path('profile/', profileView, name='profile'),
    path('search/', searchView, name='search'),
    path('admin/', adminView, name='admin')
]