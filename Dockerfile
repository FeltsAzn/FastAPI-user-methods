FROM python:3.10.6-slim
#ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY . .
RUN apt-get clean && apt-get update
RUN python3 -m pip install -r requirements.txt
EXPOSE 8080

