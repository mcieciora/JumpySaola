from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        pin_code = request.form.get('pin_code')

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.pin_code, pin_code):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect pin code, try again.', category='error')
        else:
            flash('Username does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out!', category='success')
    return redirect(url_for('auth.login'))


@auth.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        pin_code_1 = request.form.get('pin_code_1')
        pin_code_2 = request.form.get('pin_code_2')

        user = User.query.filter_by(username=username).first()
        if user:
            flash('User already exists.', category='error')
        elif len(username) < 3:
            flash('User name length must be greater than 3 characters.', category='error')
        elif pin_code_1 != pin_code_2:
            flash(r'Passwords do not match.', category='error')
        elif len(pin_code_1) != 4:
            flash('Password must be exactly 4 characters long.', category='error')
        else:
            new_user = User(username=username, pin_code=generate_password_hash(pin_code_1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)
