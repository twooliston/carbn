from flask import Flask
import os

from .extensions import db, ma

from .Routes.customer_routes import customer_blueprint
from .Routes.order_routes import order_blueprint


def create_app(config_file='settings.py'):
    #  Init app
    app = Flask(__name__)

    # Init config
    app.config.from_pyfile(config_file)

    # Init Database
    db.init_app(app)
    # Init Marshmallow
    ma.init_app(app)

    app.register_blueprint(customer_blueprint)
    app.register_blueprint(order_blueprint)

    with app.app_context():
        db.create_all()

    # run server
    if __name__ == '__main__':
        app.run(debug=True)
