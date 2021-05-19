from sqlalchemy.sql.elements import or_
from carbn_app.Models.Order import Order
from flask import Blueprint, request, jsonify

from carbn_app.extensions import db

from carbn_app.Models.Customer import Customer, CustomerSchema, FilteredCustomerSchema

# Init Schema
customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)
filtered_customers_schema = FilteredCustomerSchema(many=True)

customer_blueprint = Blueprint('customer_blueprint', __name__)


# Add New Customer
@customer_blueprint.route('/customer', methods=['POST'])
def add_customer():
    id = request.json['id']
    firstName = request.json['firstName']
    lastName = request.json['lastName']
    email = request.json['email']

    new_customer = Customer(id, firstName, lastName, email)
    db.session.add(new_customer)
    db.session.commit()
    return customer_schema.jsonify(new_customer)


# Get All Customers
@customer_blueprint.route('/customer', methods=['GET'])
def get_customers():
    all_customers = Customer.query.all()
    response = customers_schema.dump(all_customers)
    return jsonify(response)


# Update a Customer
@customer_blueprint.route('/customer/<id>', methods=['PUT'])
def update_customer(id):
    customer = Customer.query.get_or_404(id)

    customer.firstName = request.json['firstName']
    customer.lastName = request.json['lastName']
    customer.email = request.json['email']

    db.session.commit()
    return customer_schema.jsonify(customer)


# Delete a Customer
@customer_blueprint.route('/customer/<id>', methods=['DELETE'])
def delete_customer(id):
    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    return customer_schema.jsonify(customer)


# Search for a Customer
# there is no current way to determine if this will be a search or a get customer
# therefore this method will handle both
# I recommend that the search be move to a seperate route i.e. '/customer/search/<search>'
@customer_blueprint.route('/customer/<search>', methods=['GET'])
def search_customer(search):
    customer = db.session.query(Customer).join(
        Order).filter(Customer.id == search).first()

    # Hacky code to check if the records that match the customer Id exist without orders
    if customer == None:
        try:
            customer = Customer.query.get_or_404(search)
        except:
            print("No ID match")

    # if an ID matches the search return that customer
    if customer:
        return customer_schema.dump(customer)
    # else search rest of fields and return all customers containing subquery
    else:
        look_for = '%{}%'.format(search)
        all_customers = Customer.query.filter(
            or_(
                Customer.firstName.ilike(look_for),
                Customer.lastName.ilike(look_for),
                Customer.email.ilike(look_for)
            )).all()
        return jsonify(filtered_customers_schema.dump(all_customers))
