# Learn and Prep 

## Tech stack

- *Framework* : Django (Python)
- *Database* : TBD (currently sqlite3)
- *API Layer* : Django REST Framework (DRF)
- *Authentication* : TBD
- *Virtual Environment*: venv (built-in to Python)

## Development Setup

Clone the repository

    git clone https://github.com/9bit-Jedi/learn-and-prep-backend.git

Setup Virtual Environment

    py -m venv .venv
    .\'.venv'\Scripts\activate

Enter working directory

    cd .\learn-and-prep-backend\

Install dependencies

    pip install django
    pip install djangorestframework
    python -m pip install django-debug-toolbar
    
    pip install -r requirements.txt

Migrate to database

    python manage.py makemigrations

    python manage.py migrate

Create superuser

    python manage.py createsuperuser

Run Development server

    python manage.py runserver
