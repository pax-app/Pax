from project.api.utils.status_strategy import Context, InitiatedStrategy, FinalizedStrategy, CanceledStrategy, PendentStrategy
from project.api.utils.chain_of_responsibility.chain import UpCreate, UpdateState
from project.api.utils.creation_utils import Utils
from flask import request, jsonify, Blueprint
from database_singleton import Singleton
from project.api.models import Pax
from sqlalchemy import exc

pax_blueprint = Blueprint('pax', __name__)
db = Singleton().database_connection()
utils = Utils()


@pax_blueprint.route('/upCreate', methods=['POST'])
def upCreate():
    body = request.get_json()

    chat_id = body.get('chat_id')
    row = Pax.query.filter_by(chat_id=chat_id).first()

    chain = UpCreate()
    return chain.execute(request, row)


@pax_blueprint.route('/update_status', methods=['PATCH'])
def update_state():
    body = request.get_json()

    chat_id = body.get('chat_id')
    row = Pax.query.filter_by(chat_id=chat_id).first()

    chain = UpdateState()
    return chain.execute(request, row)


@pax_blueprint.route('/consult_pax/<chat_id>', methods=['GET'])
def consult_pax(chat_id):
    pax = Pax.query.filter_by(chat_id=chat_id).all()

    if not pax:
        return jsonify({'exists': 'false'}), 201

    data = [row.to_json() for row in pax]

    response = {
        'exists': 'true',
        'pax': data[0]
    }

    return jsonify(response), 201


@pax_blueprint.route('/finalized_pax/<user_kind>/<id>', methods=['GET'])
def get_finalized_pax(user_kind, id):
    try:
        context = Context(FinalizedStrategy())
        finalized_pax = context.execute_filtering(user_kind, int(id))
        if not finalized_pax:
            return jsonify(utils.createFailMessage('Cannot find user')), 404
    except ValueError:
        return jsonify(utils.createFailMessage('Cannot find user')), 404

    return jsonify(utils.createSuccessGet(finalized_pax)), 200


@pax_blueprint.route('/initiated_pax/<user_kind>/<id>', methods=['GET'])
def get_initiated_pax(user_kind, id):
    try:
        context = Context(InitiatedStrategy())
        initiated_pax = context.execute_filtering(user_kind, int(id))
        if not initiated_pax:
            return jsonify(utils.createFailMessage('Cannot find user')), 404
    except ValueError:
        return jsonify(utils.createFailMessage('Cannot find user')), 404

    return jsonify(utils.createSuccessGet(initiated_pax)), 200


@pax_blueprint.route('/canceled_pax/<user_kind>/<id>', methods=['GET'])
def get_canceled_pax(user_kind, id):
    try:
        context = Context(CanceledStrategy())
        canceled_pax = context.execute_filtering(user_kind, int(id))
        if not canceled_pax:
            return jsonify(utils.createFailMessage('Cannot find user')), 404
    except ValueError:
        return jsonify(utils.createFailMessage('Cannot find user')), 404

    return jsonify(utils.createSuccessGet(canceled_pax)), 200


@pax_blueprint.route('/pendent_pax/<user_kind>/<id>', methods=['GET'])
def get_pendent_pax(user_kind, id):
    try:
        context = Context(PendentStrategy())
        pendent_pax = context.execute_filtering(user_kind, int(id))
        if not pendent_pax:
            return jsonify(utils.createFailMessage('Cannot find user')), 404
    except ValueError:
        return jsonify(utils.createFailMessage('Cannot find user')), 404

    return jsonify(utils.createSuccessGet(pendent_pax)), 200
