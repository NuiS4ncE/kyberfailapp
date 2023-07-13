from django.urls import path, include

from .views import homePageView, noteWriteView, loginView, registerView

urlpatterns = [
    path('', homePageView, name='home'),
    path('login/', loginView, name='login'),
    path('notes/', noteWriteView, name='notewrite'),
    path('register/', registerView, name='registerView')
]