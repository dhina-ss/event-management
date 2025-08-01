from django.shortcuts import render
from rest_framework.views import APIView, status
from rest_framework.response import Response
from .models import Event
from .serializers import EventSerializer, EventAttendeesSerializer
from datetime import date
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema


class EventAPIView(APIView):

    def get(self, request):
        today = date.today()
        event = Event.objects.filter(event_date__gte=today).order_by("event_date")
        serializer = EventSerializer(event, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=EventSerializer)
    def post(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Event created successfully"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventAttendeesAPIView(APIView):

    def get(self, request, event_id):
        try:
            event = Event.objects.get(event_id=event_id)
        except Event.DoesNotExist:
            return Response(
                {"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND
            )

        attendees = event.event_attendees.all()
        paginator = PageNumberPagination()
        paginated_attendees = paginator.paginate_queryset(attendees, request)
        serializer = EventAttendeesSerializer(paginated_attendees, many=True)
        return paginator.get_paginated_response(serializer.data)


class EventAttendeesRegisterAPIView(APIView):

    @swagger_auto_schema(request_body=EventAttendeesSerializer)
    def post(self, request, event_id):
        try:
            event = Event.objects.get(event_id=event_id)
        except Event.DoesNotExist:
            return Response(
                {"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if event.event_attendees.count() >= event.max_capacity:
            return Response(
                {"error": "Event is at full capacity. Cannot register more attendees."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        email = request.data.get("attendee_email")
        if event.event_attendees.filter(attendee_email=email).exists():
            return Response(
                {"error": "This email is already registered for the event."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = EventAttendeesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(event=event)
            return Response(
                {"message": "Attendee registered successfully"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
