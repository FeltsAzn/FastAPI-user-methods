FROM python:3.10.6-slim
WORKDIR . /app
COPY requirements.txt requirements.txt
COPY . /app
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt
EXPOSE 8000

CMD ["python3", 'uvicorn', 'app/app.main:app', '--host', '0.0.0.0']
