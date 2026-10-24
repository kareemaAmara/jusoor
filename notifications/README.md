# Jusoor Backend

Volunteer Management System (VMS) — Backend API built with Django.

## Tech Stack

- Python 3.15
- Django 6.1
- Django REST Framework
- SQLite (development)

## Project Structure

backend/
- jusoor_backend/     (Project settings)
- users/              (Users & Organizations)
- opportunities/      (Volunteer opportunities & categories)
- applications/       (Applications & participation tracking)
- notifications/      (Notifications, messages & reports)
- manage.py

## Setup Instructions

### 1. Clone the repository
git clone https://github.com/kareemaAmara/jusoor.git
cd jusoor/backend

### 2. Create virtual environment
python -m venv venv
venv\Scripts\activate

### 3. Install dependencies
pip install django djangorestframework django-cors-headers Pillow

### 4. Apply migrations
python manage.py migrate

### 5. Create superuser
python manage.py createsuperuser

### 6. Run the server
python manage.py runserver

Server runs at: http://127.0.0.1:8000/
Admin panel at: http://127.0.0.1:8000/admin/

## Database Models

### Users App
- User — Custom user model (volunteer, organization, admin)
- Organization — Organization profile linked to user

### Opportunities App
- Category — Opportunity categories
- Opportunity — Volunteer opportunities

### Applications App
- Application — Volunteer applications for opportunities
- Participation — Verified volunteer hours

### Notifications App
- Notification — System notifications
- Message — Internal messages between users
- Report — Generated reports & analytics

## Team

- Bissan Walid Ali Shair — Backend
- Afnan Maher Salman Eluwity — Backend
- Karima Ismail Sulaiman Amara — Frontend
- Heba Hatem Mohammed Almassri — Frontend
- Walaa Fayez Ahmed Esleem — Frontend

Supervisor: Prof. Hatem Hammad
Islamic University of Gaza — Computer Engineering Department