from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.apiOverview, name="api-overview"),
    path('event-list/', views.eventList, name="event-list"),
    path('event-create/', views.eventCreate, name="event-create"),
    path('event-delete/<str:pk>/', views.eventDelete, name="event-delete"),
]