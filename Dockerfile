#FROM python:3.7.11-slim-buster
FROM python:3.9-slim-buster




WORKDIR /app

COPY docker/conf/sources.list /etc/apt/sources.list
COPY requirements.txt requirements.txt

RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .

#ENTRYPOINT ["uvicorn", "main:app"]
#CMD ["celery", "-A", "app.celery.tasks", "worker", "--loglevel=info"]
#CMD ["sh", "-c", "while true; do echo 1111; sleep 180; done"]

#EXPOSE ${API_PORT}
EXPOSE 8000
#ENTRYPOINT ["python", "main.py"]

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]