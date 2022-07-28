from ma import ma
from models.card import CardModel
from schemas.score import ScoreSchema


class CardSchema(ma.SQLAlchemyAutoSchema):
    score = ma.Nested(ScoreSchema, many=True)

    class Meta:
        model = CardModel
        load_instance = True
        load_only = ("user",)
        include_fk= True