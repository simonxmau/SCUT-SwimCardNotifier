from celery import Celery
from app.config import celery_config

celery_app = Celery('tasks')
celery_app.config_from_object(celery_config)
