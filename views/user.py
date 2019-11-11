# -*- coding: utf-8 -*-

from flask import (
    request, Blueprint, current_app, render_template,
    url_for, redirect, make_response, flash
)
user = Blueprint('user',
                 __name__,
                 url_prefix='/user')


@user.route('/<user_id>', endpoint='user')
def profile(user_id):
    """profile"""
    username = request.cookies.get('username')
    resp = make_response(render_template(...))
    resp.set_cookie('username', 'the username')
    return resp


@user.route('/login', endpoint='login')
def login():
    """login"""
    return render_template('login.html')


@user.route('/logout', endpoint='logout')
def logout():
    return ''


@user.route('/sign_up', endpoint='sign_up', methods=['GET', 'POST'])
def sign_up():
    """sign_up"""
    if request.method == 'POST':
        email = request.form.get('email', '')
        password_1 = request.form.get('password_1', '')
        password_2 = request.form.get('password_2', '')
        if not email:
            flash('email error.', 'danger')
            return render_template('sign_up.html')

        if not password_1 or not password_2 or password_1 != password_2:
            flash('password is not same.', 'danger')
            return render_template('sign_up.html')

        flash('sign up ok.', 'info')
        return redirect(url_for('user.login'))

    return render_template('sign_up.html')
