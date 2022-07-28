from flask import request
from flask_restplus import Resource, fields, Namespace

from models.score import ScoreModel
from schemas.score import ScoreSchema

SCORE_NOT_FOUND = "Score not found."


score_ns = Namespace('score', description='Score related operations')
scores_ns = Namespace('scores', description='Scores related operations')

score_schema = ScoreSchema()
score_list_schema = ScoreSchema(many=True)

#Model required by flask_restplus for expect
score = scores_ns.model('Score', {
    'score': fields.Integer,
    'attempts': fields.Integer,
    'card_id': fields.Integer
})


class Score(Resource):

    def get(self, id):
        score_data = ScoreModel.find_by_id(id)
        if score_data:
            return score_schema.dump(score_data)
        return {'message': SCORE_NOT_FOUND}, 404

    def delete(self,id):
        score_data = ScoreModel.find_by_id(id)
        if score_data:
            score_data.delete_from_db()
            return {'message': "Score Deleted successfully"}, 200
        return {'message': SCORE_NOT_FOUND}, 404

    @score_ns.expect(score)
    def put(self, id):
        score_data = ScoreModel.find_by_id(id)
        score_json = request.get_json()

        if score_data:
            score_data.score = score_json['score']
            score_data.attempts = score_json['attempts']
        else:
            score_data = score_schema.load(score_json)

        score_data.save_to_db()
        return score_schema.dump(score_data), 200


class ScoreList(Resource):
    @scores_ns.doc('Get all the Scores')
    def get(self):
        return score_list_schema.dump(ScoreModel.find_all()), 200

    @scores_ns.expect(score)
    @scores_ns.doc('Create an Score')
    def post(self):
        score_json = request.get_json()
        score_data = score_schema.load(score_json)
        score_data.save_to_db()

        return score_schema.dump(score_data), 201
