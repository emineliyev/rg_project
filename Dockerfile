# Используем базовый образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем зависимости системы
RUN apt-get update && apt-get install -y \
    libpq-dev gcc --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем Python-зависимости
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем весь код приложения
COPY . .

# Экспортируем порт для сервера
EXPOSE 8000

# Команда запуска сервера (разработка)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
