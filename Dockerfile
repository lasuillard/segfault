# for heroku deployment
FROM segfault:latest




CMD python manage.py runserver 0.0.0.0:$PORT
