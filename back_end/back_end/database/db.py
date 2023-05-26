from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from .redis_db import RedisDB
from .mongo_db import MongoDB

db = SQLAlchemy()
mongo = MongoDB()
mail = Mail()
redis_db = RedisDB()

# redis_store = StrictRedis(host='127.0.0.1', port=6379, db=0)

def config_database(app):
    db.init_app(app)
    mail.init_app(app)
    mongo.init_app(app)
    redis_db.init_app(app)
    with app.app_context():
        db.create_all()
