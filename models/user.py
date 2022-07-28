from db import db
from typing import List


class UserModel(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(120), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)

    cards = db.relationship("CardModel",lazy="dynamic",primaryjoin="UserModel.id == CardModel.user_id")
    def __init__(self, username, email, name, password):
        self.username = username
        self.email = email
        self.name = name
        self.password = password

    def __repr__(self):
        return 'UserModel(username=%s)' % self.username

    @classmethod
    def find_by_username(cls, username) -> "UserModel":
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id) -> "UserModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List["UserModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
