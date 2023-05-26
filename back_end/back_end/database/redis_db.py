import redis
from typing import Dict


class RedisDB:
    def __init__(self):
        self.group_name = None
        self.task_name = None
        self.r = None

    def init_app(self, app):
        self.task_name = app.config['TASK_NAME']
        self.group_name = app.config['GROUP_NAME']
        redis_pool = redis.ConnectionPool(
            host=app.config['REDIS_HOST'],
            port=app.config['REDIS_PORT'],
            password=app.config['REDIS_PASSWORD'],
            db=app.config['REDIS_DB'],
            decode_responses=True
        )
        self.r = redis.StrictRedis(connection_pool=redis_pool)

    def set_item(self, name: str, value: int, ex):
        self.r.set(name=name, value=value, ex=ex)

    def get_item(self, name):
        return self.r.get(name=name)

    def xadd(self, value: Dict):
        # if not self.r.exists(self.task_name):
        #     self.r.xadd(self.task_name, {'message': 'init'})
        #     self.r.xgroup_create(self.task_name, self.group_name, id='$')
        self.r.xadd(self.task_name, value)
