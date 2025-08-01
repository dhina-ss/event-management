from django.contrib import admin
from .models import Event, EventAttendees

admin.site.register(Event)
admin.site.register(EventAttendees)