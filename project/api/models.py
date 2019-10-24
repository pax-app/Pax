from database import db
from project import create_app
from Flask import current_app
from database_singleton import Singleton

db = Singleton().database_connection()

class Pax(db.Model):
    __tablename__ = 'PAX'
