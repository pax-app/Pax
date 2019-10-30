from flask import request, jsonify, Blueprint
from database_singleton import Singleton
from project.api.utils.creation_utils import Utils
from project.api.models import Pax
from sqlalchemy import exc

pax_blueprint = Blueprint('pax', __name__)
db = Singleton().database_connection()
utils = Utils()


@pax_blueprint.route('/receipt', methods=['POST'])
def add_receipt():
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
