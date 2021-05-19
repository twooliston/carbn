from flask import Flask
import os

from carbn_app.extensions import db, ma

from carbn_app.Routes.customer_routes import customer_blueprint
from carbn_app.Routes.order_routes import order_blueprint

#  Init app
app = Flask(__name__)

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
