from .db import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    logo = db.Column(db.Text, nullable=False)
    name = db.Column(db.String(512), nullable=False)
    description = db.Column(db.String(1024), nullable=False)

    content = db.Column(db.Text, default='')

    index = db.Column(db.Integer, index=True)
    type = db.Column(db.String(512), nullable=False)

    submit_description = db.Column(db.Text, default='')
    default_config = db.Column(db.String(1024), default='')
    allowed_file_types = db.Column(db.String(256), default='')

    def to_json(self):
        return {
            'id': self.id,
            'logo': self.logo,
            'name': self.name,
            'description': self.description,
            'index': self.index,
            'type': self.type
        }

    def to_full_json(self):
        return {
            'id': self.id,
            'logo': self.logo,
            'name': self.name,
            'description': self.description,
            'index': self.index,
            'type': self.type,
            'content': self.content
        }
