from flask import request
from flask_restplus import Resource, fields, Namespace

from models.card import CardModel
from schemas.card import CardSchema

CARD_NOT_FOUND = "Card not found."


card_ns = Namespace('card', description='Card related operations')
cards_ns = Namespace('cards', description='Cards related operations')

card_schema = CardSchema()
card_list_schema = CardSchema(many=True)

#Model required by flask_restplus for expect
card = cards_ns.model('Card', {
    'topic': fields.String('Topic of the Card'),
    'question': fields.String('Question of the Card'),
    'answer': fields.String('Answer of the Card'),
    'user_id': fields.Integer
})


class Card(Resource):

    def get(self, id):
        card_data = CardModel.find_by_id(id)
        if card_data:
            return card_schema.dump(card_data)
        return {'message': CARD_NOT_FOUND}, 404

    def delete(self,id):
        card_data = CardModel.find_by_id(id)
        if card_data:
            card_data.delete_from_db()
            return {'message': "Card Deleted successfully"}, 200
        return {'message': CARD_NOT_FOUND}, 404

    @card_ns.expect(card)
    def put(self, id):
        card_data = CardModel.find_by_id(id)
        card_json = request.get_json()

        if card_data:
            card_data.topic = card_json['topic']
            card_data.question = card_json['question']
            card_data.answer = card_json['question']
            card_data.user_id = card_json['user_id']
        else:
            card_data = card_schema.load(card_json)

        card_data.save_to_db()
        return card_schema.dump(card_data), 200


class CardList(Resource):
    @cards_ns.doc('Get all the Cards')
    def get(self):
        return card_list_schema.dump(CardModel.find_all()), 200

    @cards_ns.expect(card)
    @cards_ns.doc('Create an Card')
    def post(self):
        card_json = request.get_json()
        card_data = card_schema.load(card_json)
        card_data.save_to_db()

        return card_schema.dump(card_data), 201
