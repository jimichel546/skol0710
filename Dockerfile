FROM python:3.10-slim

WORKDIR /app

# Установка зависимостей
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Копирование зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода проекта
COPY . .

# Порт, который будет прослушивать контейнер
EXPOSE 8000

# Команда для запуска приложения
CMD ["sh", "-c", "cd testtask && python manage.py migrate && python manage.py collectstatic --noinput && uwsgi --http :8000 --module testtask.wsgi"] 