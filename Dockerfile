FROM python:3.12.6 AS backend

WORKDIR /vehicles_rental/

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

ARG DATABASE_URL
ENV DATABASE_URL=${DATABASE_URL}

COPY ./requirements.txt /vehicles_rental/

RUN pip install -r requirements.txt

COPY . /vehicles_rental/

RUN python manage.py collectstatic --no-input

EXPOSE 8080

CMD ["bash", "-c", "cd /vehicles_rental/ && python manage.py migrate && gunicorn --chdir /vehicles_rental --bind 0.0.0.0:8080 --access-logfile - --error-logfile - vehicles_rental.wsgi:application"]
