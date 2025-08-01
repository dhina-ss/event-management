from rest_framework import serializers
from .models import Event, EventAttendees

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class EventAttendeesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventAttendees
        fields = ['attendee_id', 'attendee_name', 'attendee_email']

    def validate_attendee_name(self, value):
        if not value.replace(' ', '').isalpha():
            raise serializers.ValidationError("Name should contain only letters.")
        return value