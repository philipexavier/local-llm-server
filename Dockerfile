FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    git build-essential curl && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY server.py .
COPY download_model.sh .

# Opcional: baixa o modelo automaticamente ao iniciar
# RUN chmod +x download_model.sh && ./download_model.sh

EXPOSE 8000

CMD ["python", "server.py"]
