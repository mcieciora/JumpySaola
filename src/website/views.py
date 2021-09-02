from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from .models import Transaction, Category, Period, History
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


@views.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':

        category_name = request.form.get('category_name')
        category_limit = request.form.get('category_limit')
        period_name = request.form.get('period_name')

        if category_name:
            if len(category_name) < 3:
                flash('Category name should be at least 3 characters long', category='error')
            else:
                new_category = Category(name=category_name, limit=category_limit, user_id=current_user.id)
                db.session.add(new_category)
                db.session.commit()
                flash('Category added!', category='success')

        if period_name:
            if len(current_user.categories) > 0:
                if len(period_name) < 3:
                    flash('Period name should be at least 3 characters', category='error')
                else:
                    if db.session.query(History).filter(History.name == period_name).first():
                        flash('Such period name was already used in the past!', category='error')
                    else:
                        new_period = Period(name=period_name, user_id=current_user.id)
                        db.session.add(new_period)
                        db.session.commit()
                        flash('Period started!', category='success')
            else:
                flash('You need to have at least one transaction category created before starting new period!',
                      category='error')

        if all(v is None for v in [category_name, category_limit, period_name]):
            if current_user.active_period:
                try:
                    new_history = History(name=current_user.active_period[0].name,
                                          outcomes=current_user.get_total_transaction_value(False),
                                          incomes=current_user.get_total_transaction_value(True),
                                          user_id=current_user.id)
                    db.session.add(new_history)
                    db.session.commit()
                    period = Period.query.get(current_user.active_period[0].id)
                    if period and period.user_id == current_user.id:
                        db.session.query(Transaction).delete()
                        db.session.delete(period)
                        db.session.commit()
                except:
                    db.session.rollback()

    return render_template("settings.html", user=current_user)


@views.route('/delete_transaction/<transaction_id>', methods=['DELETE'])
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


@views.route('/delete_category/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    if request.method == 'DELETE':
        try:
            category = Category.query.get(category_id)
            if category and category.user_id == current_user.id:
                db.session.delete(category)
                db.session.commit()
        except:
            db.session.rollback()


@views.route('/delete_period/<int:period_id>', methods=['DELETE'])
def delete_period(period_id):
    if request.method == 'DELETE':
        try:
            period = History.query.get(period_id)
            if period and period.user_id == current_user.id:
                db.session.delete(period)
                db.session.commit()
        except:
            db.session.rollback()
