# Learn and Prep 

## Tech stack

- *Framework* : Django (Python)
- *Database* : TBD (currently sqlite3)
- *API Layer* : Django REST Framework (DRF)
- *Authentication* : Django build-in authentication
- *Virtual Environment*: venv (built-in to Python)

## Development Setup

Clone the repository

    git clone https://github.com/9bit-Jedi/learn-and-prep-backend.git

Setup Virtual Environment

    py -m venv .venv

    .\.venv\Scripts\activate

Enter working directory

    cd .\learn-and-prep-backend\

Install dependencies
   
    pip install -r requirements.txt

Migrate to database
https://docs.djangoproject.com/en/5.0/topics/migrations/#module-django.db.migrations

    python manage.py makemigrations

    python manage.py migrate

Create superuser
https://docs.djangoproject.com/en/1.8/intro/tutorial02/#creating-an-admin-user

    python manage.py createsuperuser

Run Development server
https://docs.djangoproject.com/en/5.0/intro/tutorial01/#the-development-server

    python manage.py runserver
