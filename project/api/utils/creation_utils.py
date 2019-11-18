from database_singleton import Singleton
from flask import request, jsonify
from project.api.models import Pax
from operator import itemgetter

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
            'data': {
                'pax': [pax.to_json() for pax in content]
            }
        }
        return response_object

    def commit_to_database(self, type, model):
        if (type == 'A'):
            db.session.add(model)
        elif (type == 'M'):
            db.session.merge(model)

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

    def sqlalchemyobj_to_list(self, data):
        final_list = []
        for item in data:
            final_list.append(item.to_json())
        return final_list

    def ignore_empty_status(self, data) -> list:
        query = self.sqlalchemyobj_to_list(data)
        filtered_pax = []
        for pax in query:
            if pax['status'] != '':
                filtered_pax.append(pax)
        return filtered_pax


    def reverse_alphabetical_order(self, data: list) -> list:
        reverse_alphabetical_pax = sorted(data, key=itemgetter('status'), reverse=True)
        return reverse_alphabetical_pax
