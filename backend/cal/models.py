from django.db import models

# Create your models here.

class Event(models.Model):
    name = models.CharField(max_length=100)
    start = models.DateField()
    end = models.DateField()

    def __str__(self):
        return self.name

    def getJsonValues(self):
        eventData = {"name": self.name, "start": self.start, "end": self.end}
        return eventData
        
