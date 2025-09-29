FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/logs && chmod 755 /app/logs

RUN useradd -m -u 1000 user
USER user

CMD ["python", "bot.py"]

