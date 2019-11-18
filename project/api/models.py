from database_singleton import Singleton

db = Singleton().database_connection()


class Pax(db.Model):
    __tablename__ = 'PAX'

    pax_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    status = db.Column(db.Enum('F', 'P', 'C', 'I'), nullable=True)
    user_id = db.Column(db.Integer, nullable=False)
    provider_id = db.Column(db.Integer, nullable=False)
    chat_id = db.Column(db.Integer, nullable=False)
    address_id = db.Column(db.Integer, nullable=False)
    canceled_motive = db.Column(db.String(500), nullable=True)

    def __init__(self, date, description, name, price, status, user_id, provider_id, chat_id, address_id, canceled_motive):
        self.date = date
        self.description = description
        self.name = name
        self.price = price
        self.status = status
        self.user_id = user_id
        self.provider_id = provider_id
        self.chat_id = chat_id
        self.address_id = address_id
        self.canceled_motive = canceled_motive

    def to_json(self):
        return {
            'pax_id': self.pax_id,
            'date': self.date.isoformat(),
            'description': self.description,
            'name': self.name,
            'price': self.price,
            'status': self.status,
            'user_id': self.user_id,
            'provider_id': self.provider_id,
            'chat_id': self.chat_id,
            'address_id': self.address_id,
            'canceled_motive': self.canceled_motive,
        }
