import os
from flask import Flask, jsonify
from project.api.views import pax_blueprint
from database_singleton import Singleton


# instantiate the app
def create_app(script_info=None):
    # Instantiate the app
    app = Flask(__name__)

    # Set Configuration
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    db = Singleton().database_connection()
    migrate = Singleton().migration()

    db.init_app(app)
    migrate.init_app(app, db)

    # register blueprints
    app.register_blueprint(pax_blueprint, url_prefix='/pax')

    return app
