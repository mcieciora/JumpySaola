from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from sqlalchemy.exc import SQLAlchemyError
from .models import Transaction, Category, Period, History
from . import db

views = Blueprint('views', __name__)


def query_object_add(query_element):
    db.session.add(query_element)
    db.session.commit()


def query_object_delete(query_element):
    db.session.delete(query_element)
    db.session.commit()


def get_overall_svg():
    return [current_user.generate_all_outcomes_by_category(), current_user.generate_all_outcomes_with_limits(),
            current_user.generate_incomes_outcomes_plot()]


def get_categories_svg():
    svgs = []
    for category in current_user.categories:
        svgs.append(current_user.plot_data(category.name))
    return svgs


@views.route('/categories', methods=['GET', 'POST'])
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method != 'POST':
        if request.path == '/categories':
            return render_template("home.html", user=current_user, svgs=get_categories_svg())
        else:
            return render_template("home.html", user=current_user, svgs=get_overall_svg())

    if current_user.active_period:
        try:
            transaction_value = int(request.form.get('transaction_value'))
            transaction_desc = request.form.get('transaction_desc')
            transaction_category = request.form.get('transaction_category')
            transaction_outcome = request.form.get('transaction_outcome')

            if transaction_category == '0':
                flash('Category was not set!', category='error')
                return render_template("home.html", user=current_user, svgs=get_overall_svg())

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
    return render_template("home.html", user=current_user, svgs=get_overall_svg())


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
                except SQLAlchemyError:
                    flash('Category limit value should be a number!', category='error')

        if period_name:
            period = db.session.query(Period).filter(Period.name == period_name).first()
            if period:
                flash('There is already an active period!', category='error')
                return render_template("settings.html", user=current_user)
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
                        flash('Period finished!', category='success')
                except SQLAlchemyError:
                    db.session.rollback()
            else:
                flash('There is no active period!', category='error')
    except ValueError:
        flash('Category limit value should be a number!', category='error')

    return render_template("settings.html", user=current_user)


@views.route('/history')
@login_required
def history():
    history_chart = current_user.get_month_statistics()
    return render_template("history.html", user=current_user, svg=history_chart)


@views.route('/edit_transaction/<int:transaction_id>', methods=['POST'])
@login_required
def edit_transaction(transaction_id):
    transaction = Transaction.query.get(transaction_id)
    if request.method == 'POST':
        if transaction is None:
            flash('There is no such transaction ID!', category='error')
            return render_template("home.html", user=current_user)
        transaction_value = request.form.get('transaction_value')
        transaction_desc = request.form.get('transaction_desc')
        transaction_category = request.form.get('transaction_category')
        transaction_outcome = request.form.get('transaction_outcome')

        if all(field is None for field in [transaction_value, transaction_desc, transaction_category,
                                           transaction_outcome]):
            return render_template("edit_transaction.html", user=current_user, transaction_value=transaction.value,
                                   transaction_desc=transaction.description,
                                   transaction_category=transaction.category,
                                   transaction_outcome=transaction.outcome)

        if transaction_category == '0':
            flash('Category was not set!', category='error')
        elif len(transaction_desc) < 1:
            flash('Please insert transaction description', category='error')
        else:
            try:
                if transaction_outcome:
                    transaction.value = -abs(int(transaction_value))
                    transaction.outcome = False
                else:
                    transaction.value = abs(int(transaction_value))
                    transaction.outcome = True
                transaction.description = transaction_desc
                transaction.category = transaction_category
                db.session.commit()
                flash('Transaction was updated!')
                return render_template("home.html", user=current_user)
            except ValueError:
                flash('Transaction value should be a number!', category='error')

    return render_template("edit_transaction.html", user=current_user, transaction_value=transaction.value,
                           transaction_desc=transaction.description,
                           transaction_category=transaction.category,
                           transaction_outcome=transaction.outcome)


@views.route('/delete_transaction/<int:transaction_id>', methods=['POST'])
@login_required
def delete_transaction(transaction_id):
    if request.method == 'POST':
        try:
            transaction = Transaction.query.get(transaction_id)
            if transaction and transaction.user_id == current_user.id:
                query_object_delete(transaction)
                flash('Transaction was deleted successfully!', category='success')
            else:
                flash('There is no such transaction ID!', category='error')
        except SQLAlchemyError:
            db.session.rollback()
    return render_template("home.html", user=current_user)


@views.route('/edit_category/<int:category_id>', methods=['POST'])
@login_required
def edit_category(category_id):
    category = Category.query.get(category_id)
    category_name = request.form.get('category_name')
    category_limit = request.form.get('category_limit')
    if request.method == 'POST':
        if not category_name and not category_limit:
            return render_template("edit_category.html", user=current_user, category_name=category.name,
                                   category_limit=category.limit)
        if len(category_name) < 3:
            flash('Category name should be at least 3 characters long', category='error')
        elif category_limit == '':
            flash('Category limit shall not be empty!', category='error')
        else:
            try:
                if category.name != category_name and \
                        db.session.query(Category).filter(Category.name == category_name).first():
                    flash('Such category name already exists!', category='error')
                    return render_template("edit_category.html", user=current_user, category_name=category.name,
                                           category_limit=category.limit)
                else:
                    category.limit = int(category_limit)
                    category.name = category_name
                    db.session.commit()
                    flash('Category was updated!')
                    return render_template("settings.html", user=current_user)
            except ValueError:
                flash('Category limit value should be a number!', category='error')
        return render_template("edit_category.html", user=current_user, category_name=category.name,
                               category_limit=category.limit)


@views.route('/delete_category/<int:category_id>', methods=['POST'])
@login_required
def delete_category(category_id):
    if request.method == 'POST':
        try:
            category = Category.query.get(category_id)
            if category and category.user_id == current_user.id:
                query_object_delete(category)
                flash('Category was deleted successfully!', category='success')
            else:
                flash('There is no such category ID!', category='error')
        except SQLAlchemyError:
            db.session.rollback()
    return render_template("settings.html", user=current_user)


@views.route('/delete_period/<int:period_id>', methods=['POST'])
@login_required
def delete_period(period_id):
    if request.method == 'POST':
        try:
            period = History.query.get(period_id)
            if period and period.user_id == current_user.id:
                query_object_delete(period)
                flash('Period was deleted successfully!', category='success')
            else:
                flash('There is no such period ID!', category='error')
        except SQLAlchemyError:
            db.session.rollback()
    return render_template("history.html", user=current_user)
