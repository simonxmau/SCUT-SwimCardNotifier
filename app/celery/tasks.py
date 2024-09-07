import logging
import os

from app.config.cfg_celery import celery_app
from datetime import datetime, time

from app.lib.bot import send_error, send
from app.lib.db import Session, Order
from app.lib.hs_client import HSClient

logger = logging.getLogger('celery')


def is_within_time_range(start_time, end_time):
    now = datetime.now().time()
    return start_time <= now <= end_time


def task_with_time_check():
    return is_within_time_range(time(6, 30), time(8, 0)) or \
        is_within_time_range(time(18, 30), time(22, 0))


@celery_app.task(name='tasks.keep_session_to_live')
def keep_session_to_live():
    logger.info(f'keep_session_to_live')

    obj = Session()
    sessions = obj.get_sessions()
    for session in sessions:
        logger.info(f'get_card_count: {get_card_count.delay(session)}')
    return True


@celery_app.task(name='tasks.get_card_count')
def get_card_count(session):
    logger.info(f'get_card_count: session={session}')

    client = HSClient(session)
    return client.get_card_count()


@celery_app.task(name='tasks.cron_check')
def cron_check():
    time_limit = os.environ.get('TIME_LIMIT')
    # logger.info(f'worker 启动配置: TIME_LIMIT={time_limit}')
    if (time_limit == '1') and not task_with_time_check():
        # logger.info(f'cron_check: time limit, skip')
        return

    logger.info(f'cron_check')

    # 查询所有 session
    obj = Session()
    sessions = obj.get_sessions()
    for session in sessions:
        orders = obj.get_orders(session)
        for order in orders:
            check.delay(session, order)
    return True


@celery_app.task(name='tasks.check')
def check(session, order_no):
    logger.info(f'check: session={session}, order_no={order_no}')

    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    client = HSClient(session)

    try:
        remain = client.get_remain_enter_times(order_no)
        logger.info(f'查询结果: order_no={order_no}, remain={remain}, time={time}')

        order = Order()
        if int(order.get_last_num(order_no)) != int(remain):
            order.set_last_num(order_no, remain)
            send(order_no, remain, time)
    except Exception as e:
        send_error(e, order_no, time)
