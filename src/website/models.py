from flask_login import UserMixin
from . import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    pin_code = db.Column(db.String(150))
    active_period = db.relationship('Period')
    transactions = db.relationship('Transaction')
    categories = db.relationship('Category')
    history = db.relationship('History')

    def get_categories(self):
        categories = {}
        for category in self.categories:
            categories[category.name] = \
                {'limit': category.limit, 'value': self.get_category_transactions_value(category.name)}
        return categories

    def get_category_transactions_value(self, category, income=False):
        total = 0
        for transaction in self.transactions:
            if transaction.category == category:
                if income and transaction.value > 0:
                    total += transaction.value
                elif income is False and transaction.value < 0:
                    total += transaction.value
        return total

    def get_total_transaction_value(self, income):
        return sum([self.get_category_transactions_value(name, income) for name, values in
                    self.get_categories().items()])

    def get_total_limit(self):
        return sum([values['limit'] for name, values in self.get_categories().items()])


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer)
    description = db.Column(db.String(150))
    category = db.Column(db.String(150))
    outcome = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True)
    limit = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Period(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True)
    outcomes = db.Column(db.Integer)
    incomes = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
