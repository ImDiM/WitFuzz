from flask import Flask
from flask_cors import CORS
from back_end.api import config_blueprint
from back_end.database import config_database
from back_end import config_extensions


def create_app():
    flask_app = Flask(__name__)
    #  load config file
    flask_app.config.from_object('config_dev')
    config_extensions(flask_app)
    config_database(flask_app)
    config_blueprint(flask_app)
    #  allow cors origin
    CORS(flask_app, supports_credentials=True)
    return flask_app


app = create_app()





if __name__ == '__main__':
    app.run(
        app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )
