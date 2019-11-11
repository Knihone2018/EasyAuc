# -*- coding: utf-8 -*-

from extensions import db


class Account(db.Model):
    """Basic account model
    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True)
    firstname = db.Column(db.String(80))
    lastname = db.Column(db.String(80))
    password = db.Column(db.String(255))
    address = db.Column(db.String(80))
    bank_account_number = db.Column(db.String(255))
    is_blocked = db.Column(db.Boolean, default=False)
    is_deleted = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return "<Account %s %s>" % self.firstname, self.lastname


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, unique=True)
    quantity = db.Column(db.Integer)
    is_bid = db.Column(db.Boolean)

    def __repr__(self):
        return "<Cart%s %s>" % self.id

