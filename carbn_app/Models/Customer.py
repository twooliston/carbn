from marshmallow import fields
from sqlalchemy.orm import backref
from sqlalchemy.sql.elements import Null
from carbn_app.extensions import db, ma

from .Order import OrderSchema


# Customer Class
class Customer(db.Model):
    id = db.Column(db.String, primary_key=True)  # , unique=True
    firstName = db.Column(db.String(50))  # nullable=False
    lastName = db.Column(db.String(50))
    email = db.Column(db.String(50))
    orders = db.relationship('Order', backref='customer')  # lazy=True

    def __init__(self, id, firstName, lastName, email):
        self.id = id
        self.firstName = firstName
        self.lastName = lastName
        self.email = email


# Customer Schema
class CustomerSchema(ma.Schema):
    id = fields.Str()
    firstName = fields.Str()
    lastName = fields.Str()
    email = fields.Str()
    orders = fields.Nested(OrderSchema(many=True))


# Customer Schema
class FilteredCustomerSchema(ma.Schema):
    id = fields.Str()
    firstName = fields.Str()
    lastName = fields.Str()
    email = fields.Str()
