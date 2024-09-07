import logging

from dingtalkchatbot.chatbot import DingtalkChatbot

from app.config import cfg_bot

logger = logging.getLogger('celery')

webhook = cfg_bot.webhook
secret = cfg_bot.secret
logger.info(f'读取配置: webhook={webhook}, secret={secret}')


def send(order_no, remain, time):
    bot = DingtalkChatbot(webhook, secret)
    res = bot.send_markdown(
        title=f'{order_no} 剩余 {remain} 次',
        text=f'### **订单次数变动提醒**\n'
             f'**订单号码:**  {order_no}\n\n'
             f'**剩余次数:**  {remain}\n\n'
             f'**通知时间:**  {time}\n\n',
        is_at_all=True)
    logger.info(f'推送结果: remain={remain}, order_no={order_no}, time={time}, result={res}')


def send_error(message, order_no, time):
    bot = DingtalkChatbot(webhook, secret)
    res = bot.send_markdown(
        title=f'查询异常',
        text=f'### **{message}**\n'
             f'**订单号码:**  {order_no}\n\n'
             f'**通知时间:**  {time}\n\n',
        is_at_all=True)
    logger.info(f'推送结果: message={message}, order_no={order_no}, time={time}, result={res}')
