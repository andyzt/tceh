# -*- coding: utf-8 -*-

from flask.ext.wtf import Form
from wtforms import StringField, validators, ValidationError

__author__ = 'sobolevn'


def full_name_validator(form, field):
    name_parts = field.data.split(' ')
    if len(name_parts) < 2:
        raise ValidationError('Name is not full!')

API_validators = [{'Name': [validators.Length(min=1, max=200),],
                  'Email': [validators.Length(min=1),]},
                  {'Name': [validators.Length(min=1, max=200), full_name_validator,],
                  'Email': [validators.Length(min=1),]}]

v_version = 2


class ContactForm(Form):
    Name = StringField(label='Title', validators=[])
    Email = StringField(label='Text', validators=[])