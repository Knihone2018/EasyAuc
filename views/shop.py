# -*- coding: utf-8 -*-

from flask import (
    request, Blueprint, render_template,
    url_for, redirect, make_response, session, flash
)

shop = Blueprint('shop',
                 __name__,
                 url_prefix='/')


@shop.route('/', endpoint='shop')
def index():
    """shop index"""
    user_id = session.get('user_id')
    if not user_id:
        flash('Please login first.', 'danger')
        return redirect(url_for('user.login'))

    resp = make_response(render_template('shop.html'))
    resp.set_cookie('user_id', user_id)
    return resp
