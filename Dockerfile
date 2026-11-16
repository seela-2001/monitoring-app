FROM python:3.12-slim
WORKDIR /app
ENV PYTHONUNBUFFERED=1
COPY requirements.txt .
RUN pip install  -r requirements.txt
COPY . .
EXPOSE 8000
# worker واحد + threads: عشان الـ metrics تفضل صحيحة من غير multiprocess mode
CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 1 --threads 4"]
