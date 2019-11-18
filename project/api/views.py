from project.api.utils.status_strategy import Context, InitiatedStrategy, FinalizedStrategy, CanceledStrategy, PendentStrategy
from project.api.utils.chain_of_responsibility.chain import UpCreate, UpdateStatus
from project.api.utils.creation_utils import Utils
from flask import request, jsonify, Blueprint
from database_singleton import Singleton
from project.api.models import Pax
from sqlalchemy import exc

pax_blueprint = Blueprint('pax', __name__)
db = Singleton().database_connection()
utils = Utils()


@pax_blueprint.after_request
def add_header(r):
    """
    Adding headers to prevent page caching
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0, post-check=0, pre-check=0"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "-1"
    return r


@pax_blueprint.route('/upCreate', methods=['POST'])
def upCreate():
    body = request.get_json()

    chat_id = body.get('chat_id')
    row = Pax.query.filter_by(chat_id=chat_id).first()

    chain = UpCreate()
    return chain.execute(request, row)


@pax_blueprint.route('/update_status', methods=['PATCH'])
def update_status():
    body = request.get_json()

    chat_id = body.get('chat_id')
    row = Pax.query.filter_by(chat_id=chat_id).first()

    chain = UpdateStatus()
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


@pax_blueprint.route('/all_pax/<user_id>', methods=['GET'])
def get_all_pax(user_id):
    try:
        pax = Pax.query.filter_by(user_id=int(user_id)).all()
        pax = utils.ignore_empty_status(pax)
        pax = utils.reverse_alphabetical_order(pax)
        if not pax:
            return jsonify(utils.createFailMessage('Cannot find user')), 404
    except ValueError:
        return jsonify(utils.createFailMessage('Cannot find user')), 404
    return jsonify(pax), 200


@pax_blueprint.route('/cancel_pax', methods=['PATCH'])
def cancel_pax():
    post_data = request.get_json()

    chat_id = post_data.get('chat_id')
    canceled_motive = post_data.get('canceled_motive')

    pax = Pax.query.filter_by(chat_id=chat_id).first()
    if not pax:
        return jsonify(utils.createFailMessage('Inexistent Pax')), 404

    pax.status = 'C'
    pax.canceled_motive = canceled_motive
    utils.commit_to_database('M', pax)

    return jsonify(utils.createSuccessMessage('Updated canceled motive!')), 200
