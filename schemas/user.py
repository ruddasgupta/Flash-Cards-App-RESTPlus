from ma import ma
from models.user import UserModel
from schemas.card import CardSchema


class UserSchema(ma.SQLAlchemyAutoSchema):
    cards = ma.Nested(CardSchema, many=True)

    class Meta:
        model = UserModel
        load_instance = True
        include_fk = True
