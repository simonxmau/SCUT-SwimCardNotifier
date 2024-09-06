import os
from dotenv import load_dotenv
from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dingtalkchatbot.chatbot import DingtalkChatbot
from datetime import datetime
import logging

import order_api
from last_remain import LastRemain

logger = logging.getLogger('uvicorn')
app = FastAPI()
scheduler = AsyncIOScheduler()

load_dotenv()
order_no = os.environ.get('ORDER_NO')
session = os.environ.get('SESSION')
webhook = os.environ.get('WEBHOOK')
secret = os.environ.get('SECRET')
logger.info(f'读取配置: order_no={order_no}, session={session}, webhook={webhook}, secret={secret}')


@app.on_event("startup")
async def startup_event():
    logger.info("FastAPI 服务启动")

    logger.info("定时任务启动")
    scheduler.start()


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("FastAPI 服务关闭")

    scheduler.shutdown()
    logger.info("定时任务关闭")

# @app.post("/add_url")
# def add_url(data: dict):
#     url = data.get('url')
#     task = tasks.get_item.delay(url)
#     # print('task', task.get())
#     return url

# # 设置在每天 6:30 到 8:00 之间每分钟运行一次
# @scheduler.scheduled_job(trigger=CronTrigger(hour='6', minute='30-59'))
# @scheduler.scheduled_job(trigger=CronTrigger(hour='7', minute='0-59'))
# async def morning_task():
#     logger.info("This job runs every minute between 6:30 and 8:00.")
#     check()
#
# @scheduler.scheduled_job(trigger=CronTrigger(hour='12', minute='30-59'))
# async def midday_task():
#     logger.info("This job runs every minute between 6:30 and 8:00.")
#     check()
#
# # 设置在每天 18:30 到 22:00 之间每分钟运行一次
# @scheduler.scheduled_job(trigger=CronTrigger(hour='18', minute='30-59'))
# @scheduler.scheduled_job(trigger=CronTrigger(hour='19-21', minute='0-59'))
# @scheduler.scheduled_job(trigger=CronTrigger(hour='22', minute='0-0'))
# async def evening_task():
#     logger.info("This job runs every minute between 18:30 and 22:00.")
#     check()


# 会阻塞
@scheduler.scheduled_job('interval', seconds=1 * 60)
async def check() -> None:
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        remain = order_api.get_remain_enter_times(order_api.get_order_detail(order_no=order_no, session=session))
        logger.info(f'查询结果: order_no={order_no}, remain={remain}, time={time}')
        if LastRemain().get() != int(remain):
            LastRemain().save(remain)
            send(order_no, remain, time)
    except Exception as e:
        send_error(e, time)


# 不阻塞
# scheduler.add_job(task1, 'interval', seconds=1)


def send(order_no, remain, time):
    bot = DingtalkChatbot(webhook, secret)
    res = bot.send_markdown(
        title=f'{order_no} 剩余 {remain} 次',
        text=f'### **订单次数变动提醒**\n'
             f'**订单号码:**  {order_no}\n\n'
             f'**剩余次数:**  {remain}\n\n'
             f'**检查时间:**  {time}\n\n',
        is_at_all=True)
    logger.info(f'推送结果: {res}')


def send_error(message, time):
    bot = DingtalkChatbot(webhook, secret)
    res = bot.send_markdown(
        title=f'查询异常',
        text=f'### **{message}**\n'
             f'**订单号码:**  {order_no}\n\n'
             f'**检查时间:**  {time}\n\n',
        is_at_all=True)
    logger.info(f'推送结果: {res}')
