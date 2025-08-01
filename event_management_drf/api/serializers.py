from rest_framework import serializers
from .models import Event, EventAttendees
from pytz import timezone


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"
        read_only_fields = ["event_id"]

    def get_event_start_time(self, obj):
        if obj.event_start_time:
            return obj.event_start_time.astimezone(timezone("Asia/Kolkata")).isoformat()
        return None

    def get_event_end_time(self, obj):
        if obj.event_end_time:
            return obj.event_end_time.astimezone(timezone("Asia/Kolkata")).isoformat()
        return None


class EventAttendeesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventAttendees
        fields = ["attendee_id", "attendee_name", "attendee_email"]
        read_only_fields = ["attendee_id"]

    def validate_attendee_name(self, value):
        if not value.replace(" ", "").isalpha():
            raise serializers.ValidationError("Name should contain only letters.")
        return value
