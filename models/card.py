from datetime import datetime
from db import db
from typing import List


class CardModel(db.Model):
    __tablename__ = "card"

    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(100))
    question = db.Column(db.String(100000))
    answer = db.Column(db.String(100000))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    user_id =db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    user = db.relationship("UserModel",)

    scores = db.relationship("ScoreModel",lazy="dynamic",primaryjoin="CardModel.id == ScoreModel.card_id")

    def __init__(self, topic, question, answer, user_id):
        self.topic = topic
        self.question = question
        self.answer = answer
        self.user_id = user_id

    def __repr__(self):
        return 'CardModel(topic=%s, question=%s, answer=%s, user_id=%s)' % (self.topic, self.question, self.answer, self.user_id)

    def json(self):
        return {'topic': self.topic, 'question': self.question, 'answer': self.answer}

    @classmethod
    def find_by_id(cls, _id) -> "CardModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List["CardModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
