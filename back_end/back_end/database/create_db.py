from .db import db


def config_database(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
