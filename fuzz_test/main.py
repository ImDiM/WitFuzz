import redis
from configparser import ConfigParser
from fuzz_test import afl_easy_test, afl_dumb_test, afl_quick_test, afl_standard_test
from util import save_result, start_test
from db import MySQLDB, MongoDB
import json
import os


def run(config, mysql_db: MySQLDB, mongo_db: MongoDB):
    if not os.path.exists('tmp'):
        os.mkdir('tmp')
    pool = redis.ConnectionPool(
        host=config['app']['REDIS_HOST'],
        port=config['app']['REDIS_PORT'],
        db=config['app']['REDIS_DB'],
        password=config['app']['REDIS_PASSWORD'],
        decode_responses=True
    )
    r = redis.StrictRedis(connection_pool=pool)

    task_name = config['app']['TASK_NAME']

    print('=== test server started ===', flush=True)
    while True:
        ret = r.xread({task_name: '0-0'}, count=1, block=0)
        message_id = ret[0][1][0][0]
        message_data = json.loads(ret[0][1][0][1]['message'])
        r.xdel(task_name, *[message_id])

        print('--- message ---', flush=True)
        print(message_data, flush=True)

        start_test(
            mysql_db=mysql_db,
            record_id=message_data['data']['record_id']
        )
        if message_data['task_name'] == 'AFL-Easy':
            afl_easy_test(mysql_db=mysql_db, mongo_db=mongo_db, data=message_data['data'])
        elif message_data['task_name'] == 'AFL-Standard':
            afl_standard_test(mysql_db=mysql_db, mongo_db=mongo_db, data=message_data['data'])
        elif message_data['task_name'] == 'AFL-Quick':
            afl_quick_test(mysql_db=mysql_db, mongo_db=mongo_db, data=message_data['data'])
        elif message_data['task_name'] == 'AFL-Dumb':
            afl_dumb_test(mysql_db=mysql_db, mongo_db=mongo_db, data=message_data['data'])
        else:
            save_result(
                mysql_db=mysql_db,
                record_id=message_data['data']['record_id'],
                result='',
                status='failed',
                running_time='0 s',
                result_file_id=''
            )


if __name__ == '__main__':
    config = ConfigParser()
    config.read('config_dev.ini')
    mysql_db = MySQLDB(config)
    mongo_db = MongoDB(config)
    run(config, mysql_db, mongo_db)
