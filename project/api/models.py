from database import db
from project import create_app
from Flask import current_app


class Pax(db.Model):
    __tablename__ = 'PAX'
