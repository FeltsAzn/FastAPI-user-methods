FROM python:3.10.6-slim

ENV PYTHONUNBUFFERED 1

EXPOSE 8080
WORKDIR /app

COPY . /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ['bash', '-c', 'uvicorn', 'app:app', '--port 8080']
