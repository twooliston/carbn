from flask import Blueprint, request, jsonify

from extensions import db

from Models.Customer import Customer
from Models.Order import Order, OrderSchema

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
    db.session.add(new_order)
    db.session.commit()

    return order_schema.jsonify(new_order)


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

    order.date = request.json['date']
    order.amount = request.json['amount']

    db.session.commit()
    return order_schema.jsonify(order)