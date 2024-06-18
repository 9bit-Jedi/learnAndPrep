# Learn and Prep 

## Tech stack

- *Framework* : Django (Python)
- *Database* : TBD (currently sqlite3)
- *API Layer* : Django REST Framework (DRF)
- *Authentication* : Django build-in authentication
- *Virtual Environment* : venv (built-in to Python)
- *Docker* : now Dockerised

## Git Pull

pull the desired branch

    git pull origin main

change branch on local 

    git checkout <branch_name>
    
Install (updated) dependencies
   
    pip install -r requirements.txt

Run Development server
https://docs.djangoproject.com/en/5.0/intro/tutorial01/#the-development-server

    python manage.py runserver

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

Migrate & Create super user (Only if recreating DB)
https://docs.djangoproject.com/en/5.0/topics/migrations/#module-django.db.migrations

    python manage.py makemigrations
    python manage.py migrate
    python manage.py createsuperuser

Run Development server
https://docs.djangoproject.com/en/5.0/intro/tutorial01/#the-development-server

    python manage.py runserver
