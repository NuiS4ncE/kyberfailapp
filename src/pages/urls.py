from django.urls import path, include

from .views import homePageView, noteWriteView, loginView

urlpatterns = [
    path('', homePageView, name='home'),
    path('login/', loginView, name='login'),
    path('notes/', noteWriteView, name='notewrite'),
]