from django.db import models

class Event(models.Model):
    event_id = models.CharField(max_length=50, primary_key=True)
    event_name = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    event_date = models.DateField(null=True)
    event_start = models.TimeField(null=True)
    event_end = models.TimeField(null=True)
    max_capacity = models.IntegerField(default=10000)

    def __str__(self):
        return self.event_name
    
class EventAttendees(models.Model):
    event = models.ForeignKey('Event', on_delete=models.CASCADE, related_name='event_attendees')
    attendee_id = models.CharField(max_length=50)
    attendee_name = models.CharField(max_length=100)
    attendee_email = models.EmailField(null=True)