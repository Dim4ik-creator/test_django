FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app


COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY projec/ .
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD gunicorn --workers 4 --bind 0.0.0.0:8000 projec.wsgi:application
# CMD ["gunicorn", "--workers", "4" , "--bind", "0.0.0.0:8000", "projec.wsgi:application", ]