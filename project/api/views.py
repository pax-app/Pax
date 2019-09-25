from flask import request, jsonify, Blueprint

pax_blueprint = Blueprint('pax', __name__)


@pax_blueprint.route('/pax/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })
