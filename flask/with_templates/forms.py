# -*- coding: utf-8 -*-

from flask.ext.wtf import Form
from wtforms import StringField, validators, ValidationError

__author__ = 'sobolevn'



class ContactForm(Form):
    title = StringField(label='Title', validators=[
        validators.Length(min=1, max=200),
    ])
    text = StringField(label='Text', validators=[
        validators.Length(min=1),
    ])
