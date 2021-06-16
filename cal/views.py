from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from cal.models import Event
from django.core import serializers
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def index(request):
    if (request.method == "GET"):
        all_events = Event.objects.all()
        json_events = []
        for event in all_events:
            json_events.append(event.getJsonValues())
        return JsonResponse({"events": json_events})
    elif (request.method == "DELETE"):
        event_dict = json.loads(request.body)

        name = event_dict["name"]
        start = event_dict["start"]
        end = event_dict["end"]

        response = Event.objects.filter(
            name=name, start=start, end=end).delete()
        return HttpResponse(response)
    elif (request.method == "POST"):
        event_dict = json.loads(request.body)
        print(event_dict)

        name = event_dict["name"]
        start = event_dict["start"]
        end = event_dict["end"]

        event_to_add = Event(name=name, start=start, end=end)
        event_to_add.save()
        return HttpResponse("posting event")