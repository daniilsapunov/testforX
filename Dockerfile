# Используем официальный образ Python
FROM python:3.12-slim

# Установка зависимостей
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Задаем директорию для приложения
WORKDIR /app

# Копируем файлы зависимостей
COPY requirements.txt /app/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы приложения
COPY . /app/

# Команда для запуска сервера
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "linkstorage.wsgi:application"]