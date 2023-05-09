python manage.py migrate
exec uvicorn friendsservice.asgi:application --host 0.0.0.0 --reload