from datetime import datetime
from db import db
from typing import List


class ScoreModel(db.Model):
    __tablename__ = "score"

    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer)
    attempts = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    card_id =db.Column(db.Integer,db.ForeignKey('card.id'),nullable=False)
    card = db.relationship("CardModel",)

    def __init__(self, score, attempts, card_id):
        self.score = score
        self.attempts = attempts
        self.card_id = card_id

    def __repr__(self):
        return 'ScoreModel(score=%s, attempts=%s, card_id=%s)' % (self.score, self.attempts, self.card_id)

    def json(self):
        return {'score': self.score, 'attempts': self.attempts}

    @classmethod
    def find_by_id(cls, _id) -> "ScoreModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List["ScoreModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
