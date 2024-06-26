FROM python:slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "manage.py", "makemigrations"]
CMD ["python", "manage.py", "migrate"]
# CMD ["python", "manage.py", "createsuperuser"]
# docker exec -it container_id python manage.py createsuperuser
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

EXPOSE 8000

# first build using 
