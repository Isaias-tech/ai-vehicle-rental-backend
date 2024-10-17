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

# Install cron
RUN apt-get update && apt-get install -y cron

# Copy the cron job configuration
COPY cronjob /etc/cron.d/vehicles_rental_cron

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/vehicles_rental_cron

# Apply the cron job
RUN crontab /etc/cron.d/vehicles_rental_cron

RUN touch /vehicles_rental/logs/cron.log

# Ensure cron is started and the Django app runs
CMD ["bash", "-c", "cd /vehicles_rental/ && python manage.py migrate && cron && gunicorn --chdir /vehicles_rental --bind 0.0.0.0:8080 --access-logfile - --error-logfile - vehicles_rental.wsgi:application"]
