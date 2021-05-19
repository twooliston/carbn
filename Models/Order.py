from extensions import db, ma

from sqlalchemy.dialects.mysql import FLOAT

# Order Class


class Order(db.Model):
    id = db.Column(db.String, primary_key=True)
    customer_id = db.Column(db.String, db.ForeignKey(
        'customer.id'))
    date = db.Column(db.Date)
    amount = db.Column(FLOAT(precision=10, scale=2))

    def __init__(self, id, customer_id, date, amount):
        self.id = id
        self.customer_id = customer_id
        self.date = date
        self.amount = amount


# Order Schema
class OrderSchema(ma.Schema):
    class Meta:
        fields = ('id', 'customer_id', 'date', 'amount')
