from .db import db


class Problem(db.Model):
    __tablename__ = 'problem'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(512), nullable=False)
    description = db.Column(db.Text, nullable=False)
    answer_number = db.Column(db.Integer, default=0, index=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'answer_number': self.answer_number,
            'user_id': self.user_id
        }