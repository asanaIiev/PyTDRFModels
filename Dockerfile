FROM python:3.12-slim

ENV DJANGO_SETTINGS_MODULE=settings.settings.settings

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cpu

COPY . .

CMD ["uvicorn", "settings.settings.asgi:application", "--host", "0.0.0.0", "--port", "8000"]