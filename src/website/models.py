from flask_login import UserMixin
from pygal import Pie, SolidGauge
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

    def generate_default_plot(self):
        return_list = []
        if (total := self.get_total_limit()) > 0:
            gauge = SolidGauge(inner_radius=0.50)
            gauge.add('Total expanse with limit', [{'value': self.get_total_transaction_value(False) * -1,
                                                    'max_value': total}],
                      formatter=lambda x: '{:.10g} PLN'.format(x))
            return_list.append(gauge.render_data_uri())
            del gauge
        if (total := self.get_total_transaction_value(True)) > 0:
            gauge = SolidGauge(inner_radius=0.50)
            gauge.add('Total outcome with income',
                      [{'value': self.get_total_transaction_value(False) * -1, 'max_value': total}],
                      formatter=lambda x: '{:.10g} PLN'.format(x))
            return_list.append(gauge.render_data_uri())
        return return_list

    def plot_data(self, category):
        category_data = self.get_categories()[category]
        if category_data['value'] < 0:
            category_data['value'] = category_data['value'] * -1
        gauge = SolidGauge(inner_radius=0.50)
        gauge.add(category, [{'value': category_data['value'], 'max_value': category_data['limit']}],
                  formatter=lambda x: '{:.10g} PLN'.format(x))
        return gauge.render_data_uri()


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
