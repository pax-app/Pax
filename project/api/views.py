from project.api.utils.status_strategy import Context, InitiatedStrategy, FinalizedStrategy, CanceledStrategy, PendentStrategy
from project.api.utils.creation_utils import Utils
from flask import request, jsonify, Blueprint
from database_singleton import Singleton
from project.api.models import Pax
from sqlalchemy import exc

pax_blueprint = Blueprint('pax', __name__)
db = Singleton().database_connection()
utils = Utils()


@pax_blueprint.route('/upCreate_pax', methods=['POST'])
def upCreate():
    pax = request.get_json()

    if not pax:
        return jsonify(utils.createFailMessage('Wrong JSON')), 400

    date = pax.get('date')
    description = pax.get('description')
    name = pax.get('name')
    price = pax.get('price')
    user_id = pax.get('user_id')
    provider_id = pax.get('provider_id')
    chat_id = pax.get('chat_id')
    address_id = pax.get('address_id')

    row = Pax.query.filter_by(chat_id=chat_id).first()

    if row is None:
        try:
            pax = Pax(date, description, name,
                      price, '', user_id, provider_id, chat_id, address_id)
            utils.commit_to_database('A', pax)
            return jsonify(utils.createSuccessMessage('Pax was created!')), 201

        except exc.IntegrityError:
            db.session.rollback()
            return jsonify(utils.createFailMessage('Wrong JSON')), 400

    try:
        row.date = date
        row.description = description
        row.name = name
        row.price = price
        row.address_id = address_id

        utils.commit_to_database('M', row)
        return jsonify(utils.createSuccessMessage('Pax was updated!')), 201

    except exc.IntegrityError:
        db.session.rollback()
        return jsonify(utils.createFailMessage('Wrong JSON')), 400


@pax_blueprint.route('/consult_pax', methods=['GET'])
def consult_pax():
    chat_id = request.args.get('chat_id')

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
