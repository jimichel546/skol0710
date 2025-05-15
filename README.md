# JSON Uploader

Проект для загрузки и валидации JSON файлов с последующим сохранением данных в MySQL.

## Требования

- Debian 11+
- Python 3.8+
- MySQL 5.7+
- Nginx
- uWSGI

## Инструкция по развертыванию

### Вариант 1: Развертывание с использованием Docker

Наиболее простой способ запустить приложение - использовать Docker и Docker Compose.

#### Предварительные требования

- Docker
- Docker Compose

#### Шаги по развертыванию

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/jimichel546/skol0710.git
   cd json-uploader
   ```

2. Запустите контейнеры:
   ```bash
   docker-compose up -d
   ```

3. Приложение будет доступно по адресу http://localhost

4. Остановка контейнеров:
   ```bash
   docker-compose down
   ```

5. Если вы хотите удалить данные:
   ```bash
   docker-compose down -v
   ```

### Вариант 2: Ручное развертывание на сервере

### 1. Установка необходимых пакетов

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv mysql-server nginx
sudo apt install -y python3-dev default-libmysqlclient-dev build-essential
```

### 2. Создание базы данных MySQL

```bash
sudo mysql -u root -p
```

В консоли MySQL:

```sql
CREATE DATABASE mydb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'root'@'localhost' IDENTIFIED BY 'root';
GRANT ALL PRIVILEGES ON mydb.* TO 'root'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 3. Настройка проекта

```bash
# Клонирование репозитория
git clone <URL репозитория> /var/www/jsonuploader
cd /var/www/jsonuploader

# Создание виртуального окружения
python3 -m venv venv
source venv/bin/activate

# Установка зависимостей
pip install django==5.2.1 mysqlclient uwsgi

# Миграция базы данных
cd testtask
python manage.py migrate

# Сбор статических файлов
python manage.py collectstatic
```

### 4. Настройка uWSGI

Создайте файл `/var/www/jsonuploader/uwsgi.ini`:

```ini
[uwsgi]
project = testtask
base = /var/www/jsonuploader

chdir = %(base)
home = %(base)/venv
module = %(project).wsgi:application

master = true
processes = 5

socket = /var/www/jsonuploader/%(project).sock
chmod-socket = 664
vacuum = true

die-on-term = true
```

### 5. Создание systemd сервиса для uWSGI

Создайте файл `/etc/systemd/system/uwsgi_jsonuploader.service`:

```ini
[Unit]
Description=uWSGI Service for JSON Uploader
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/jsonuploader
ExecStart=/var/www/jsonuploader/venv/bin/uwsgi --ini /var/www/jsonuploader/uwsgi.ini
Restart=always
KillSignal=SIGQUIT
Type=notify
NotifyAccess=all

[Install]
WantedBy=multi-user.target
```

Запустите сервис:

```bash
sudo systemctl start uwsgi_jsonuploader
sudo systemctl enable uwsgi_jsonuploader
```

### 6. Настройка Nginx

Создайте файл `/etc/nginx/sites-available/jsonuploader`:

```nginx
server {
    listen 80;
    server_name your_domain_or_ip;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /var/www/jsonuploader/testtask;
    }

    location / {
        include uwsgi_params;
        uwsgi_pass unix:/var/www/jsonuploader/testtask.sock;
    }
}
```

Создайте символическую ссылку и перезапустите Nginx:

```bash
sudo ln -s /etc/nginx/sites-available/jsonuploader /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

### 7. Настройка файрвола

```bash
sudo ufw allow 'Nginx Full'
```

### 8. Проверка

Откройте в браузере http://your_domain_or_ip и убедитесь, что сайт работает корректно.

## Дополнительно

### Обновление кода

Для обновления кода проекта:

```bash
cd /var/www/jsonuploader
git pull
source venv/bin/activate
cd testtask
python manage.py migrate
python manage.py collectstatic --no-input
sudo systemctl restart uwsgi_jsonuploader
```

### Просмотр логов

```bash
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
sudo journalctl -u uwsgi_jsonuploader
``` 
