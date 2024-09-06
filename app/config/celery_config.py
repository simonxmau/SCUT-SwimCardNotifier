import os

from app.config.celery_beat_schedule import BEAT_SCHEDULE

broker_url = os.environ.get('CELERY_BROKER')
result_backend = os.environ.get('CELERY_BACKEND')
broker_connection_retry_on_startup = True
task_reject_on_worker_lost = True
task_acks_late = True
worker_hijack_root_logger = False  # disable default logging
timezone = 'Asia/Shanghai'
beat_schedule = BEAT_SCHEDULE
