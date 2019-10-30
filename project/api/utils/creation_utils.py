from database_singleton import Singleton
from flask import request, jsonify
from project.api.models import Pax

db = Singleton().database_connection()


class Utils:
    def createFailMessage(self, message):
        response_object = {
            'status': 'fail',
            'message': '{}'.format(message)
        }
        return response_object

    def createSuccessMessage(self, message):
        response_object = {
            'status': 'success',
            'message': '{}'.format(message)
        }
        return response_object

    def createSuccessGet(self, content):
        response_object = {
            'status': 'success',
            'data': content
        }
        return response_object

    def commit_to_database(self, model):
        db.session.add(model)
        db.session.flush()
        db.session.commit()

    def filter_by_status(self, value, user_type, id):
        if user_type == 'provider':
            pax = Pax.query.filter_by(
                status=value, provider_id=int(id)).all()
        elif user_type == 'user':
            pax = Pax.query.filter_by(
                status=value, user_id=int(id)).all()
        return pax
