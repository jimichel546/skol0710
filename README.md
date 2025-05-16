# JSON Uploader

Проект для загрузки и валидации JSON файлов с последующим сохранением данных в MySQL.

## Требования

- Debian 11+
- Python 3.8+
- MySQL 5.7+
- Nginx
- uWSGI

## Инструкция по развертыванию

### Развертывание с использованием Docker

Наиболее простой способ запустить приложение - использовать Docker и Docker Compose.

#### Предварительные требования

- Docker
- Docker Compose

#### Шаги по развертыванию

1. Клонируйте репозиторий:
   ```bash
   mkdir <Создайте папку под проект>
   git clone https://github.com/jimichel546/skol0710.git 
   cd skol0710
   ```

2. Запустите контейнеры:
   ```bash
   sudo docker compose up -d для новых версий
   sudo docker-compose up -d для старых версий

   ```

3. Приложение будет доступно по адресу http://localhost

4. Остановка контейнеров:
   ```bash
   sudo docker compose stop
   ```

5. Если вы хотите удалить данные:
   ```bash
   sudo docker compose down -v
   ```

