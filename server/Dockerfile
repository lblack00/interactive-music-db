FROM python:3.11-slim
WORKDIR /app

ARG FLASK_ENV=production
ARG PORT=5001

ENV FLASK_ENV=$FLASK_ENV
ENV PORT=$PORT

RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE $PORT

CMD if [ "$FLASK_ENV" = "testing" ]; then \
      echo "Running in test mode" && \
      python3 -m unittest discover -s test -p "test_*.py" -b; \
    else \
      echo "Running in production mode" && \
      python3 app.py; \
    fi