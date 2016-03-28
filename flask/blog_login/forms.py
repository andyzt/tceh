# -*- coding: utf-8 -*-

from flask.ext.wtf import Form
from wtforms_alchemy import model_form_factory
from wtforms import PasswordField, StringField
from wtforms.validators import Email, length

from models import User, Post

BaseModelForm = model_form_factory(Form)


def passwords_match(form, field):
    if form.password.data != field.data:
        raise ValueError('Passwords do not match')


class RegisterForm(BaseModelForm):
    class Meta:
        model = User

        only = ['username', 'email']

        validators = {
            'email': [Email()],
        }

    password = PasswordField()
    repeat_password = PasswordField(validators=[
        passwords_match,
    ])


class LoginForm(Form):
    username = StringField()
    password = PasswordField()

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self, *args, **kwargs):
        rv = super(LoginForm, self).validate()
        if not rv:
            return False

        user = User.query.filter_by(
            username=self.username.data).first()
        if user is None:
            self.username.errors.append('Unknown username')
            return False

        if not user.check_password(self.password.data):
            self.password.errors.append('Invalid password')
            return False

        self.user = user
        return True


class AddPostForm(BaseModelForm):
    class Meta:
        model = Post

        only = ['title', 'content']

        validators = {
            'title': [length(min=1)],
        }