from django.urls import path, include

from .views import homePageView, noteWriteView, loginView

urlpatterns = [
    path('', homePageView, name='home'),
    path('notes/', noteWriteView, name='notewrite'),
]