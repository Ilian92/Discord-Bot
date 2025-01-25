FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .env main.py commands.json ./
COPY cogs/ ./cogs/

RUN python -m pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

CMD python main.py