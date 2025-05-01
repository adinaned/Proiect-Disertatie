from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from configs.database import Config
from routes import get_all_routes
from models import db
from flask_cors import CORS

API_URL = '/swagger_config.json'
SWAGGER_URL = '/api/v1/docs'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': "Software Voting Machine API"})


def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True)

    @app.route('/swagger_config.json')
    def doc():
        return open('configs/swagger_config.json').read()

    app.register_blueprint(SWAGGERUI_BLUEPRINT)

    for blueprint in get_all_routes():
        app.register_blueprint(blueprint)

    app.config.from_object(Config)
    db.init_app(app)

    return app
