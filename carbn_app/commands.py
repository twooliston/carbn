import click
from flask.cli import with_appcontext

from .extensions import db
from .Models.Customer import Customer, CustomerSchema
from .Models.Order import Order, OrderSchema


@click.command(name="create_tables")
@with_appcontext
def create_tables():
    db.create_all()
