from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Transaction
from . import db

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        try:
            transaction_value = int(request.form.get('transaction_value'))
            transaction_desc = request.form.get('transaction_desc')
            transaction_outcome = request.form.get('transaction_outcome')

            if transaction_outcome:
                if transaction_value > 0:
                    transaction_value = transaction_value*-1
                transaction_outcome = False
            else:
                transaction_outcome = True
            if len(transaction_desc) < 1:
                flash('Please insert transaction description', category='error')
            else:
                new_transaction = Transaction(value=transaction_value, description=transaction_desc,
                                              outcome=transaction_outcome, user_id=current_user.id)
                db.session.add(new_transaction)
                db.session.commit()
                flash('Transaction added!', category='success')
        except ValueError:
            flash('Transaction value should be a number!', category='error')

    return render_template("home.html", user=current_user)


@views.route('/delete_transaction/<int:transaction_id>', methods=['DELETE'])
@login_required
def delete_transaction(transaction_id):
    if request.method == 'DELETE':
        try:
            transaction = Transaction.query.get(transaction_id)
            if transaction and transaction.user_id == current_user.id:
                db.session.delete(transaction)
                db.session.commit()
                flash('Transaction was deleted successfully!', category='success')
        except:
            db.session.rollback()
        return render_template("home.html", user=current_user)
