# -*- coding: utf-8 -*-

from datetime import date, datetime
from app import db

from werkzeug.security import (
    generate_password_hash,
    check_password_hash,
)


class User(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(20), unique=True, index=True)
    password = db.Column('password', db.String(10))
    email = db.Column('email', db.String(50), unique=True, index=True)
    registered_on = db.Column('registered_on', db.DateTime)

    def __init__(self, username=None, email=None):
        self.username = username
        # we do not store original password.
        self.email = email
        self.registered_on = datetime.utcnow()

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<%s>' % self.username


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(
        'User', backref=db.backref('posts', lazy='dynamic')
    )

    title = db.Column(db.String(140), unique=True)
    content = db.Column(db.String(3000))

    date_created = db.Column(db.Date, default=date.today())
    is_visible = db.Column(db.Boolean, default=True)

    def __init__(self, title='', content='', user=None,
                 date_created=None, is_visible=None):
        self.title = title
        self.content = content
        self.user = user

        if date_created is not None:
            self.date_created = date_created

        if is_visible is not None:
            self.is_visible = is_visible