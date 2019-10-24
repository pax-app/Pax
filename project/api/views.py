from flask import request, jsonify, Blueprint
from database_singleton import Singleton

pax_blueprint = Blueprint('pax', __name__)
db = Singleton().database_connection()


@pax_blueprint.route('/pax/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })
