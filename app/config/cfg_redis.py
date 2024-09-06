import os
# import redis
from redis import Redis


redis_host = os.environ.get('REDIS_HOST')
redis_port = os.environ.get('REDIS_PORT')
redis_db = os.environ.get('REDIS_DB')

redis_conn = Redis(host=redis_host, port=redis_port, db=redis_db, decode_responses=True)
