from dotenv import load_dotenv

load_dotenv()

from app.config.cfg_redis import redis_conn
from app.config.cfg_celery import celery_app