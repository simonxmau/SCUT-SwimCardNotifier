from app.config import redis_conn as redis


class Session:

    def add_session(self, session):
        return redis.lpush('session::all', session)

    def get_sessions(self):
        return redis.lrange('session::all', 0, -1)

    def add_order(self, session, order_no):
        return redis.lpush(f'session::order_no::{session}', order_no)

    def get_orders(self, session):
        return redis.lrange(f'session::order_no::{session}', 0, -1)


class Order:

    def get_last_num(self, order_no):
        return int(redis.get(f'order::last_num::{order_no}') or '0')

    def set_last_num(self, order_no, num):
        return redis.set(f'order::last_num::{order_no}', str(num))
