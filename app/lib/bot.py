import logging

from dingtalkchatbot.chatbot import DingtalkChatbot

from app.config import cfg_bot

logger = logging.getLogger('celery')

webhook = cfg_bot.webhook
secret = cfg_bot.secret
logger.info(f'读取配置: webhook={webhook}, secret={secret}')


def send(order_no, remain, time, at_id='', at_all=False):
    title = f'{mask_order_number(order_no)} 剩余 {remain} 次'
    text = f'''
### **订单次数变动提醒**

**订单号码:** {mask_order_number(order_no)}

**剩余次数:** {remain}

**通知时间:** {time}

'''

    dingtalk_ids = []
    if at_id:
        dingtalk_ids = [at_id]
        text = text + f'@{at_id}'

    bot = DingtalkChatbot(webhook, secret)
    res = bot.send_markdown(title=title, text=text, is_at_all=at_all, at_dingtalk_ids=dingtalk_ids)
    logger.info(f'推送结果: remain={remain}, order_no={order_no}, time={time}, result={res}')


def send_error(message, order_no, time):
    bot = DingtalkChatbot(webhook, secret)
    res = bot.send_markdown(
        title=f'查询异常',
        text=f'### **{message}**\n'
             f'**订单号码:**  {mask_order_number(order_no)}\n\n'
             f'**通知时间:**  {time}\n\n',
        is_at_all=True)
    logger.info(f'推送结果: message={message}, order_no={order_no}, time={time}, result={res}')


def mask_order_number(order_number, mask_char='*', visible_digits=4):
    """
    对订单号码进行打码处理，保留头4位和尾4位数字以便辨识。

    :param order_number: 订单号码（字符串形式）
    :param mask_char: 用于打码的字符，默认为 '*'
    :param visible_digits: 保留的可见数字位数，默认为 4
    :return: 打码后的订单号码
    """
    if not isinstance(order_number, str):
        order_number = str(order_number)

    head_visible_part = order_number[:visible_digits]
    tail_visible_part = order_number[-visible_digits:]
    masked_part = mask_char * (len(order_number) - 2 * visible_digits)

    return head_visible_part + masked_part + tail_visible_part