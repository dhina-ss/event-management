# Mini Event Management System API

A backend system built with Django REST Framework to manage events and attendees. This project provides RESTful APIs to create events, register attendees, view attendees per event, and ensures clean architecture, scalability, and data integrity.

---

# Features

- Create and list upcoming events
- Register attendees with unique email per event
- Prevent overbooking using max capacity
- Auto-generate event & attendee IDs (e.g., E001, A001)
- Pagination on attendee lists
- Timezone support (IST to UTC)
- Swagger/OpenAPI interactive API docs
- Unit tests using pytest

---

# Technologies Used

- Python 3.x
- Django 4.x
- Django REST Framework
- SQLite (default) or PostgreSQL
- drf-yasg (for Swagger docs)
- pytest (for testing)
- pytz (for timezone handling)

---

# Setup Instructions

# 1. Clone the repo

# bash
- git clone https://github.com/dhina-ss/event-management.git
- cd event-management-system

---

# 2. Create a virtual environment and activate

- python -m venv venv
- source venv/bin/activate  # or venv\Scripts\activate on Windows

# 3. Install dependencies

- pip install -r requirements.txt

# 4. Apply migrations

- python manage.py migrate

# 5. Run the development server

- python manage.py runserver

---

# API Endpoints

| Method | Endpoint                        | Description                                  |
| ------ | ------------------------------- | -------------------------------------------- |
| POST   | `/events/`                      | Create a new event                           |
| GET    | `/events/`                      | List all upcoming events                     |
| POST   | `/events/{event_id}/register/`  | Register attendee for event (email required) |
| GET    | `/events/{event_id}/attendees/` | List registered attendees (paginated)        |

---

# Sample Requests

# Create Event

POST /events/
Content-Type: application/json

{
  "event_name": "Tech Conference",
  "location": "Chennai",
  "event_date": "2025-08-10",
  "event_start": "2025-08-10T10:00:00",
  "event_end": "2025-08-10T12:00:00",
  "max_capacity": 100
}

# Register Attendee

POST /events/E001/register/
Content-Type: application/json

{
  "attendee_name": "Dhinakaran Sekar",
  "attendee_email": "dhina@example.com"
}

---

# API Documentation (Swagger)

Once server is running:

http://localhost:8000/swagger/,
http://localhost:8000/redoc/

---

# Running Unit Tests

- pytest

---

# Contributors

- Dhinakaran Sekar - Developer

---