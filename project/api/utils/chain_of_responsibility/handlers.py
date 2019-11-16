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


class UpdateHandler(AbstractHandler):
    def handle(self, request, row):
        try:
            pax = request.get_json()

            row.date = pax.get('date')
            row.description = pax.get('description')
            row.name = pax.get('name')
            row.price = pax.get('price')
            row.address_id = pax.get('address_id')

            utils.commit_to_database('M', row)
            return jsonify(utils.createSuccessMessage('Pax was updated!')), 201

        except:
            return super().handle(request, row)


class UpdateStatusHandler(AbstractHandler):
    def handle(self, request, row):
        try:
            body = request.get_json()

            status = body.get('status')

            row.status = status

            utils.commit_to_database('M', row)
            return jsonify(utils.createSuccessMessage('Pax state was updated!')), 201
        except:
            return super().handle(request, row)


class ErrorHandler(AbstractHandler):
    def handle(self, request, row):
        db.session.rollback()
        return jsonify(utils.createFailMessage('Wrong JSON')), 400
