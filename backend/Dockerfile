FROM python:3.8.5

WORKDIR /code

COPY . .

RUN pip3 install -r requirements.txt

# RUN python3 manage.py makemigrations

# RUN python3 manage.py migrate

CMD gunicorn backend.wsgi:application --bind 0.0.0.0:8000