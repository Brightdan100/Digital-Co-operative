from flask import Flask

from app import api_blueprint
from model import db


def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)

    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    db.init_app(app)

    return app


if __name__ == '__main__':
    app = create_app('config')
    app.run(debug=True)
