from django.shortcuts import render

# Create your views here.
from cal.models import Event
from cal.serializers import EventSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Event

@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'List':'/event-list/',
        # 'Detail View':'/event-list/<str:pk>/',
        'Create':'/event-create/',
        'Delete':'/event-delete/<str:pk>/'
    }
    return Response(api_urls)

@api_view(['GET'])
def eventList(request):
    events = Event.objects.all()
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def eventCreate(request):
    serializer = EventSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def eventDelete(request, pk):
    event = Event.objects.get(id=pk)
    event.delete()
    return Response('Item successfully deleted!')