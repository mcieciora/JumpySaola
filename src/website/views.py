from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from .models import Transaction, Category, Period, History
from . import db

views = Blueprint('views', __name__)


def query_object_add(query_element):
    db.session.add(query_element)
    db.session.commit()


def query_object_delete(query_element):
    db.session.delete(query_element)
    db.session.commit()


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method != 'POST':
        return render_template("home.html", user=current_user)

    if current_user.active_period:
        try:
            transaction_value = int(request.form.get('transaction_value'))
            transaction_desc = request.form.get('transaction_desc')
            transaction_category = request.form.get('transaction_category')
            transaction_outcome = request.form.get('transaction_outcome')

            if transaction_category == '0':
                flash('Category was not set!', category='error')
                return render_template("home.html", user=current_user)

            if transaction_outcome:
                transaction_value = -abs(transaction_value)
                transaction_outcome = False
            else:
                transaction_value = abs(transaction_value)
                transaction_outcome = True

            if len(transaction_desc) < 1:
                flash('Please insert transaction description', category='error')
            else:
                new_transaction = Transaction(value=transaction_value, description=transaction_desc,
                                              category=transaction_category, outcome=transaction_outcome,
                                              user_id=current_user.id)
                query_object_add(new_transaction)
                flash('Transaction added!', category='success')

        except ValueError:
            flash('Transaction value should be a number!', category='error')
    else:
        flash('No period started!', category='error')

    return render_template("home.html", user=current_user)


@views.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method != 'POST':
        return render_template("settings.html", user=current_user)

    try:
        category_name = request.form.get('category_name')
        category_limit = request.form.get('category_limit')
        period_name = request.form.get('period_name')

        if category_name:
            if len(category_name) < 3:
                flash('Category name should be at least 3 characters long', category='error')
            elif category_limit == '':
                flash('Category limit shall not be empty!', category='error')
            else:
                try:
                    if db.session.query(Category).filter(Category.name == category_name).first():
                        flash('Such category name already exists!', category='error')
                    else:
                        category_limit = int(category_limit)
                        new_category = Category(name=category_name, limit=category_limit, user_id=current_user.id)
                        query_object_add(new_category)
                        flash('Category added!', category='success')
                except:
                    flash('Category limit value should be a number!', category='error')

        if period_name:
            if len(current_user.categories) > 0:
                if len(period_name) < 3:
                    flash('Period name should be at least 3 characters', category='error')
                else:
                    if db.session.query(History).filter(History.name == period_name).first():
                        flash('Such period name was already used in the past!', category='error')
                    else:
                        new_period = Period(name=period_name, user_id=current_user.id)
                        query_object_add(new_period)
                        flash('Period started!', category='success')
            else:
                flash('You need to have at least one transaction category created before starting new period!',
                      category='error')

        if all(field is None for field in [category_name, category_limit, period_name]):
            if current_user.active_period:
                try:
                    new_history = History(name=current_user.active_period[0].name,
                                          outcomes=current_user.get_total_transaction_value(False),
                                          incomes=current_user.get_total_transaction_value(True),
                                          user_id=current_user.id)
                    query_object_add(new_history)
                    period = Period.query.get(current_user.active_period[0].id)
                    if period and period.user_id == current_user.id:
                        db.session.query(Transaction).delete()
                        query_object_delete(period)
                except:
                    db.session.rollback()
    except ValueError:
        flash('Category limit value should be a number!', category='error')

    return render_template("settings.html", user=current_user)


@views.route('/delete_transaction/<int:transaction_id>', methods=['POST'])
@login_required
def delete_transaction(transaction_id):
    if request.method == 'POST':
        try:
            transaction = Transaction.query.get(transaction_id)
            if transaction and transaction.user_id == current_user.id:
                query_object_delete(transaction)
                flash('Transaction was deleted successfully!', category='success')
        except:
            db.session.rollback()
    return render_template("home.html", user=current_user)


@views.route('/delete_category/<int:category_id>', methods=['POST'])
@login_required
def delete_category(category_id):
    if request.method == 'POST':
        try:
            category = Category.query.get(category_id)
            if category and category.user_id == current_user.id:
                query_object_delete(category)
                flash('Category was deleted successfully!', category='success')
        except:
            db.session.rollback()
    return render_template("settings.html", user=current_user)
