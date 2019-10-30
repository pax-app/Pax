from flask import request, jsonify, Blueprint
from database_singleton import Singleton
from project.api.utils.creation_utils import Utils
from project.api.models import Pax
from sqlalchemy import exc
from project.api.utils.status_strategy import Context, InitiatedStrategy, FinalizedStrategy, CanceledStrategy, PendentStrategy

pax_blueprint = Blueprint('pax', __name__)
db = Singleton().database_connection()
utils = Utils()


@pax_blueprint.route('/create_pax', methods=['POST'])
def add_pax():
    post_data = request.get_json()

    if not post_data:
        return jsonify(utils.createFailMessage('Wrong JSON')), 400

    pax = post_data.get('pax')

    data = pax.get('data')
    description = pax.get('description')
    name = pax.get('name')
    price = pax.get('price')
    status = pax.get('status')
    user_id = pax.get('user_id')
    provider_id = pax.get('provider_id')
    chat_id = pax.get('chat_id')
    address_id = pax.get('address_id')

    try:
        pax = Pax(data, description, name,
                  price, status, user_id, provider_id, chat_id, address_id)
        utils.commit_to_database(pax)
        return jsonify(utils.createSuccessMessage('Pax was created!')), 201

    except exc.IntegrityError:
        db.session.rollback()
        return jsonify(utils.createFailMessage('Wrong JSON')), 400


@pax_blueprint.route('/finalized_pax/<user_kind>/<id>', methods=['GET'])
def get_finalized_pax(user_kind, id):
    try:
        context = Context(FinalizedStrategy())
        finalized_pax = context.execute_filtering(user_kind, int(id))
        if not finalized_pax:
            return jsonify(utils.createFailMessage('Cannot find user')), 404
    except ValueError:
        return jsonify(utils.createFailMessage('Cannot find user')), 404

    return jsonify(utils.createSuccessGet(finalized_pax.to_json())), 200


@pax_blueprint.route('/initiated_pax/<user_kind>/<id>', methods=['GET'])
def get_initiated_pax(user_kind, id):
    try:
        context = Context(InitiatedStrategy())
        initiated_pax = context.execute_filtering(user_kind, int(id))
        if not initiated_pax:
            return jsonify(utils.createFailMessage('Cannot find user')), 404
    except ValueError:
        return jsonify(utils.createFailMessage('Cannot find user')), 404

    return jsonify(utils.createSuccessGet(initiated_pax.to_json())), 200


@pax_blueprint.route('/canceled_pax/<user_kind>/<id>', methods=['GET'])
def get_canceled_pax(user_kind, id):
    try:
        context = Context(CanceledStrategy())
        canceled_pax = context.execute_filtering(user_kind, int(id))
        if not canceled_pax:
            return jsonify(utils.createFailMessage('Cannot find user')), 404
    except ValueError:
        return jsonify(utils.createFailMessage('Cannot find user')), 404

    return jsonify(utils.createSuccessGet(canceled_pax.to_json())), 200
