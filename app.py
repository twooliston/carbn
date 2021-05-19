from flask import Flask
import os

from extensions import db, ma

from Routes.customer_routes import customer_blueprint
from Routes.order_routes import order_blueprint

#  Intit app
app = Flask(__name__)

# Database Location
basedir = os.path.abspath(os.path.dirname(__file__))
# Database Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
