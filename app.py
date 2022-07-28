from flask import Flask, Blueprint, jsonify
from flask_restplus import Api
from ma import ma
from db import db

from resources.user import User, UserList, user_ns, users_ns
from resources.card import Card, CardList, card_ns, cards_ns
from resources.score import Score, ScoreList, score_ns, scores_ns
from marshmallow import ValidationError

app = Flask(__name__)
bluePrint = Blueprint('api', __name__, url_prefix='/api')
api = Api(bluePrint, doc='/doc', title='Flash Card Application')
app.register_blueprint(bluePrint)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

api.add_namespace(card_ns)
api.add_namespace(cards_ns)
api.add_namespace(user_ns)
api.add_namespace(users_ns)
api.add_namespace(score_ns)
api.add_namespace(scores_ns)


@app.before_first_request
def create_tables():
    db.create_all()


@api.errorhandler(ValidationError)
def handle_validation_error(error):
    return jsonify(error.messages), 400

score_ns.add_resource(Score, '/<int:id>')
scores_ns.add_resource(ScoreList, "")
card_ns.add_resource(Card, '/<int:id>')
cards_ns.add_resource(CardList, "")
user_ns.add_resource(User, '/<int:id>')
users_ns.add_resource(UserList, "")

if __name__ == '__main__':
    db.init_app(app)
    ma.init_app(app)
    app.run(port=5001, debug=True,host='0.0.0.0')
