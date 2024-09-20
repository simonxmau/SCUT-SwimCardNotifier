import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
import logging

from app.lib.db import Session

logger = logging.getLogger('uvicorn')

app = FastAPI()

load_dotenv()
# API_PORT = os.environ.get('API_PORT')
# LOG_LEVEL = os.environ.get('LOG_LEVEL')
# logger.info(f'API 配置: API_PORT={API_PORT}, LOG_LEVEL={LOG_LEVEL}')


@app.post("/add")
def add(data: dict):
    session = data.get('session')
    order_no = data.get('order_no')
    user_id = data.get('user_id')

    if not session and not order_no:
        return '参数不完整'

    s = Session()
    s.add_session(session)
    s.add_order(session, order_no)
    s.add_userid(session, user_id)

    return '添加成功'


# if __name__ == "__main__":
#     config = uvicorn.Config("main:app", host='127.0.0.1', port=int(API_PORT), log_level=LOG_LEVEL)
#     server = uvicorn.Server(config)
#     server.run()
