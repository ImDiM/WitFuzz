from .db import db


class Record(db.Model):
    __tablename__ = 'record'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    submitted_at = db.Column(db.String(32), nullable=False)
    started_at = db.Column(db.String(32), nullable=True)
    finished_at = db.Column(db.String(32), nullable=True)
    running_time = db.Column(db.String(512), default='')
    status = db.Column(db.String(32), default='waiting')  # waiting running finished failed
    is_public = db.Column(db.Boolean, default=False)
    config_str = db.Column(db.String(1024), default='{}')
    file_id = db.Column(db.String(64), nullable=False)
    file_name = db.Column(db.String(512), nullable=False)

    description = db.Column(db.String(1024), default='')

    result_file_id = db.Column(db.String(64), nullable=True)
    out = db.Column(db.Text, default='')
    err = db.Column(db.Text, default='')

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))

    def to_json(self):
        return {
            'id': self.id,
            'status': self.status,
            'submitted_at': self.submitted_at,
            'started_at': self.started_at,
            'finished_at': self.finished_at,
            'running_time': self.running_time,
            'is_public': self.is_public,
            'config_str': self.config_str,
            'description': self.description
        }

    def to_full_json(self):
        return {
            'id': self.id,
            'status': self.status,
            'submitted_at': self.submitted_at,
            'started_at': self.started_at,
            'finished_at': self.finished_at,
            'running_time': self.running_time,
            'is_public': self.is_public,
            'config_str': self.config_str,
            'description': self.description,
            'file_id': self.file_id,
            'file_name': self.file_name,
            'result_file_id': self.result_file_id,
            'out': self.out,
            'err': self.err
        }
