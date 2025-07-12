FROM python:3.11-slim

WORKDIR /app

# Установка зависимостей системы
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    libffi-dev \
    libglib2.0-0 \
    libgdk-pixbuf2.0-0 \
    libpangocairo-1.0-0 \
    libpango-1.0-0 \
    libcairo2 \
    libxml2 \
    libxslt1.1 \
    libjpeg-dev \
    zlib1g-dev \
    netcat-openbsd \
    fonts-liberation \
    fonts-dejavu \
    && rm -rf /var/lib/apt/lists/*

# Установка зависимостей Python
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Копирование кода проекта
COPY . .

# Добавление скрипта запуска
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]# Открываем порт
EXPOSE 8000

# Запуск через gunicorn
CMD ["gunicorn", "DjangoProject1.wsgi:application", "--bind", "0.0.0.0:8000"]
