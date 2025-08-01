import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from .models import Event, EventAttendees
from datetime import date, time

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def sample_event():
    return Event.objects.create(
        event_id="EVT001",
        event_name="Test Conference",
        location="Chennai",
        event_date=date.today(),
        event_start=time(9, 0),
        event_end=time(17, 0),
        max_capacity=2
    )

@pytest.mark.django_db
def test_successful_registration(client, sample_event):
    url = reverse('attendees-register', args=[sample_event.event_id])
    data = {
        "attendee_id": "A001",
        "attendee_name": "Ravi",
        "attendee_email": "ravi@example.com"
    }
    response = client.post(url, data)
    assert response.status_code == 201
    assert EventAttendees.objects.filter(attendee_email="ravi@example.com").exists()

@pytest.mark.django_db
def test_duplicate_email_registration(client, sample_event):
    EventAttendees.objects.create(
        event=sample_event,
        attendee_id="A002",
        attendee_name="Ravi",
        attendee_email="ravi@example.com"
    )
    url = reverse('attendees-register', args=[sample_event.event_id])
    data = {
        "attendee_id": "A003",
        "attendee_name": "Ravi 2",
        "attendee_email": "ravi@example.com"  # same email
    }
    response = client.post(url, data)
    assert response.status_code == 400
    assert "already registered" in response.json()["error"]

@pytest.mark.django_db
def test_registration_when_event_full(client, sample_event):
    EventAttendees.objects.create(event=sample_event, attendee_id="A001", attendee_name="A", attendee_email="a@example.com")
    EventAttendees.objects.create(event=sample_event, attendee_id="A002", attendee_name="B", attendee_email="b@example.com")

    url = reverse('attendees-register', args=[sample_event.event_id])
    data = {
        "attendee_id": "A003",
        "attendee_name": "C",
        "attendee_email": "c@example.com"
    }
    response = client.post(url, data)
    assert response.status_code == 400
    assert "full capacity" in response.json()["error"]

@pytest.mark.django_db
def test_registration_for_non_existent_event(client):
    url = reverse('attendees-register', args=["INVALID_ID"])
    data = {
        "attendee_id": "A004",
        "attendee_name": "D",
        "attendee_email": "d@example.com"
    }
    response = client.post(url, data)
    assert response.status_code == 404
    assert "not found" in response.json()["error"]
