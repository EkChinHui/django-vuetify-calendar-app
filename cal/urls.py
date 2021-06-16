from django.urls import include, path
from django.contrib import admin

from . import views

urlpatterns = [
    path('calendar/', views.index, name='cal.urls'),
    path('test', views.test, name='cal.urls'),
]