# Використовуємо базовий образ Python
FROM python:3.10

# Встановлюємо робочу директорію
WORKDIR /app

# Копіюємо серверний код у контейнер
COPY server.py /app/server.py

# Встановлюємо необхідні залежності
RUN pip install numpy

# Відкриваємо порт для сервера
EXPOSE 65432

# Вказуємо команду для запуску сервера
CMD ["python", "server.py"]
