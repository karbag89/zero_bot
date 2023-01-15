FROM python:3.9

WORKDIR /app
COPY app /app
COPY requirements.txt /app

RUN pip install --upgrade pip && \
    python -m pip install --no-cache-dir -r requirements.txt

EXPOSE 5000
