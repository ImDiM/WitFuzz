from .db import db



class Answer(db.Model):
    __tablename__ = 'answer'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    edit_time = db.Column(db.DateTime, nullable=False, index=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    problem_id = db.Column(db.Integer, db.ForeignKey('problem.id'))
    def to_json(self):
        return {
            'id': self.id,
            'content': self.content,
            'edit_time': self.edit_time,
            'user_id': self.user_id,
            'problem_id': self.problem_id
        }