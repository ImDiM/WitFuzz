from .db import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(512), nullable=False)
    email = db.Column(db.String(512), nullable=False)
    password = db.Column(db.String(512), nullable=False)
    submit_amount = db.Column(db.Integer,nullable=True)
    intro=db.Column(db.String(512), nullable=True)
    job = db.Column(db.String(512), nullable=True)
    birthday = db.Column(db.Date, nullable=True)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'password': self.password,
            'submit_amount': self.submit_amount,
            'intro': self.intro,
            'job': self.job,
            'birthday': self.birthday
        }
