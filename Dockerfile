
# устанавливается версия образа python из репозиторич Docker Hub. Версию можно уточнить.
FROM python:3.13-slim-bullseye

# тут устанавливаем переменные среды. Первая переменная запрещает создание .pyc файлов(меньше размер образа). вторая отключает буферизацию вывода python
ENV PYTHONDONTWRITEBITECODE=1  
ENV PYTHONUNBUFFERED=1

# Устанавливаем рабочую директорию внутри контейнера. Если её нет, docker создает её сам
WORKDIR /app
# или можно так
RUN mkdir /aboba
RUN cd /aboba

# возвращаемся из примера в /app
RUN cd /app

# Копируем requirements.txt в рабочую директорию и устанавливаем зависимости.
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в рабочую директорию
COPY . /app/

# открываем порт для внешних подключений
EXPOSE 9675

# а тут просто запускаем программу из консоли bash
CMD ["python", "main.py"] 
