from .user import user
from .task import task, tasklist
from .record import record, recordlist
from .forum import forum
DEFAULT_BLUEPRINT = (
    (user, '/user'),
    (task, '/task'),
    (record, '/record'),
    (tasklist, '/tasklist'),
    (recordlist, '/recordlist'),
    (forum, '/forum')
    
)


def config_blueprint(app):
    for blueprint, prefix in DEFAULT_BLUEPRINT:
        app.register_blueprint(blueprint, url_prefix=prefix)
