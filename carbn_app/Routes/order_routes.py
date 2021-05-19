from flask import Blueprint, request, jsonify

from carbn_app.extensions import db

from carbn_app.Models.Customer import Customer
from carbn_app.Models.Order import Order, OrderSchema

import datetime

# Init Schema
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

order_blueprint = Blueprint('order_blueprint', __name__)


# Add New Order for a Customer
@order_blueprint.route('/customer/<customer_id>/order', methods=['POST'])
def add_order(customer_id):
    print(customer_id)
    customer = Customer.query.get_or_404(customer_id)
    id = request.json['id']
    date = request.json['date']
    amount = request.json['amount']

    date = datetime.datetime.strptime(date, "%d%m%Y").date()

    new_order = Order(id, customer.id, date, amount)

    try:
        db.session.add(new_order)
        db.session.commit()
        return order_schema.jsonify(new_order)
    except:
        raise Exception("Could not commit a new order to database")


# Get All Orders
@order_blueprint.route('/order', methods=['GET'])
def get_orders():
    all_orders = Order.query.all()
    response = orders_schema.dump(all_orders)
    return jsonify(response)


# Get an Order
@order_blueprint.route('/order/<id>', methods=['GET'])
def get_order(id):
    order = Order.query.get_or_404(id)
    return order_schema.jsonify(order)


# Get a Customer's Orders
@order_blueprint.route('/customer/<customer_id>/order', methods=['GET'])
def get_customer_orders(customer_id):
    all_orders = Order.query.filter_by(customer_id=customer_id).all()
    response = orders_schema.dump(all_orders)
    return jsonify(response)


# Update an Order
@order_blueprint.route('/order/<id>', methods=['PUT'])
def update_order(id):
    order = Order.query.get_or_404(id)

    # TODO: if no value keep saved value
    order.date = request.json['date']
    order.amount = request.json['amount']

    try:
        db.session.commit()
        return order_schema.jsonify(order)
    except:
        raise Exception("Could not update order from the database")


# Delete a Order
@order_blueprint.route('/order/<id>', methods=['DELETE'])
def delete_order(id):
    order = Order.query.get_or_404(id)
    try:
        db.session.delete(order)
        db.session.commit()
        return order_schema.jsonify(order)
    except:
        raise Exception("Could not delete order from database")
