# mail
MAIL_SERVER = "smtp.163.com"
MAIL_USE_SSL = True
MAIL_PORT = 465
MAIL_USERNAME = "xxx@163.com"
MAIL_PASSWORD = "xxx"
MAIL_DEFAULT_SENDER = "xxx@163.com"

# flask
HOST = '0.0.0.0'
PORT = 5000
DEBUG = True

# mysql
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://xxx:xxx@xxx:xxx/witfuzz'

# mongodb
MONGO_HOST = 'xxx'
MONGO_PORT = 0
MONGO_USER = 'xxx'
MONGO_PASSWORD = 'xxx'
MONGO_DB = 'witfuzz'

# redis
REDIS_HOST = 'xxx'
REDIS_PASSWORD = 'xxx'
REDIS_PORT = 0
REDIS_DB = 0
TASK_NAME = 'fuzz_task'
GROUP_NAME = 'fuzz_task_group'
