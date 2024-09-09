from celery.schedules import crontab

BEAT_SCHEDULE = {
    'add-every-1-minute': {
        'task': 'tasks.keep_session_to_live',
        'schedule': crontab(minute='*/15'),
    },
    'add-every-30-seconds': {
        'task': 'tasks.cron_check',
        'schedule': 30.0,
    },
}
