FROM python:3.10.6-slim
#ENV PYTHONUNBUFFERED 1
COPY . .
WORKDIR .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000

CMD ['uvicorn', 'app.main:app', '--host', '0.0.0.0']
