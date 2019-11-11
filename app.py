# -*- coding: utf-8 -*-

import logging
from flask import Flask, jsonify

from extensions import db
import models
from views import user, shop, cart


def create_app(config_object='settings'):
    app = Flask(__name__)
    app.config.from_object(config_object)
    app.logger.setLevel(logging.INFO)

    db.init_app(app)

    app.register_blueprint(user)
    app.register_blueprint(shop)
    app.register_blueprint(cart)

    if app.config.get('ENV') == 'DEV':
        db.create_all(app=app)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host=app.config.get('HOST'),
            port=app.config.get('PORT'),
            debug=app.config.get('DEBUG'))
