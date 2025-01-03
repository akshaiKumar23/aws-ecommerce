FROM python:3.9-slim


WORKDIR /app


COPY . /app

RUN pip install --no-cache-dir -r requirements.txt


RUN python manage.py collectstatic --noinput


EXPOSE 8000


CMD ["gunicorn", "aws_ecommerce.wsgi:application", "--bind", "0.0.0.0:8000"]
