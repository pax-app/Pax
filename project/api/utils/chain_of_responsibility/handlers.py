from project.api.utils.chain_of_responsibility.definitions import AbstractHandler
from project.api.utils.creation_utils import Utils
from database_singleton import Singleton
from project.api.models import Pax
from flask import jsonify

db = Singleton().database_connection()
utils = Utils()


class CreateHandler(AbstractHandler):
    def handle(self, request, row):
        if not row:
            pax = request.get_json()

            date = pax.get('date')
            description = pax.get('description')
            name = pax.get('name')
            price = pax.get('price')
            user_id = pax.get('user_id')
            provider_id = pax.get('provider_id')
            chat_id = pax.get('chat_id')
            address_id = pax.get('address_id')

            pax = Pax(date, description, name,
                      price, '', user_id, provider_id, chat_id, address_id)
            utils.commit_to_database('A', pax)
            return jsonify(utils.createSuccessMessage('Pax was created!')), 201

        else:
            return super().handle(request, row)
