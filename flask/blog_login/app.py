# -*- coding: utf-8 -*-

from flask import Flask, request, flash, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager


import config

login_manager = LoginManager()
app = Flask(__name__, template_folder='templates')
app.config.from_object(config)


db = SQLAlchemy(app)


@login_manager.user_loader
def load_user(user_id):
    from models import User

    return User.query.get(user_id)



@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('auth.login'))
    # return 'Unauthorized', 401


if __name__ == '__main__':
    from models import *
    from views import auth, views
    # Blueprints:
    app.register_blueprint(auth)
    app.register_blueprint(views)

    db.create_all()

# Custom modules:
    login_manager.init_app(app)
    app.run()

