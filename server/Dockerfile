FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY ../requirements.txt /app/
RUN pip install --no-cache-dir -r ../requirements.txt

COPY . /app/

EXPOSE 5001

CMD ["python3", "app.py"]