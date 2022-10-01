FROM python:3.10.6-slim
ENV PYTHONUNBUFFERED 1
COPY ./requirements.txt .
COPY . .
RUN apt-get clean && apt-get update
RUN apt add postgresql-dev gcc python3-dev musl-dev
RUN pip install --no-cache-dir --upgrade -r requirements.txt
EXPOSE 8080

CMD ['uvicorn', 'app.main:app', '--port', '8080']
