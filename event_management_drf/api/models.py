from django.db import models
from pytz import timezone
from django.utils.timezone import make_aware


class Event(models.Model):
    event_id = models.CharField(max_length=50, primary_key=True, editable=False)
    event_name = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    event_date = models.DateField(null=True)
    event_start_time = models.DateTimeField(null=True)
    event_end_time = models.DateTimeField(null=True)
    max_capacity = models.IntegerField(default=10000)

    def save(self, *args, **kwargs):
        if not self.event_id:
            last_event = Event.objects.order_by("-event_id").first()
            if last_event and last_event.event_id[1:].isdigit():
                last_number = int(last_event.event_id[1:])
            else:
                last_number = 0
            self.event_id = f"E{last_number + 1:03d}"

        ist = timezone("Asia/Kolkata")
        if self.event_start_time and self.event_start_time.tzinfo is None:
            self.event_start_time = make_aware(self.event_start_time, ist).astimezone(
                timezone("UTC")
            )
        if self.event_end_time and self.event_end_time.tzinfo is None:
            self.event_end_time = make_aware(self.event_end_time, ist).astimezone(
                timezone("UTC")
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.event_name


class EventAttendees(models.Model):
    event = models.ForeignKey(
        "Event", on_delete=models.CASCADE, related_name="event_attendees"
    )
    attendee_id = models.CharField(max_length=50, primary_key=True, editable=False)
    attendee_name = models.CharField(max_length=100)
    attendee_email = models.EmailField(null=True)

    def save(self, *args, **kwargs):
        if not self.attendee_id:
            last_attendee = EventAttendees.objects.order_by("-attendee_id").first()
            if last_attendee and last_attendee.attendee_id[1:].isdigit():
                last_number = int(last_attendee.attendee_id[1:])
            else:
                last_number = 0
            self.attendee_id = f"A{last_number + 1:03d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.attendee_name
