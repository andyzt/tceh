# -*- coding: utf-8 -*-

from flask import Flask, request, render_template
from flask.ext.wtf import Form
from wtforms import StringField, IntegerField, validators, ValidationError
import wtforms_json

import config

import os


app = Flask(__name__, template_folder='templates')
app.config.from_object(config)

API_validators = [{'client.name': [validators.Length(min=1),],
                  'order.count': [validators.number_range(min=1,max=5),],
                  'order.product_name': [validators.any_of(['potatoes','apples','cherries']),],
                  'client.full_address': [validators.Length(min=1),],
                   },
                  {'client.name': [validators.Length(min=1),],
                  'order.count': [validators.number_range(min=1,max=10),],
                  'order.product_name': [validators.any_of(['potatoes','apples','cherries']),],
                  'client.address.full_address': [validators.Length(min=1),],
                  'client.email': [validators.Length(min=1),validators.Email(),]
                   }
                  ]




@app.route('/api/<version>/order', methods=['POST'])
def home(version):
    def flatten_dict(dd, separator='.', prefix=''):
        return { prefix + separator + k if prefix else k : v
                 for kk, vv in dd.items()
                 for k, v in flatten_dict(vv, separator, kk).items()
                 } if isinstance(dd, dict) else { prefix : dd }

    class F(Form):
        pass

    wtforms_json.init()
    v_version = int(version[1])

    for name, validtrs in API_validators[v_version-1].items():
        setattr(F, name, StringField(label=name, validators=validtrs))

    jsondata = request.get_json()
    flatten_json=flatten_dict(jsondata)

    form = F.from_json(flatten_json)

    res = form.validate()
    for field, errors in form.errors.items():
        for error in errors:
            print(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))
    if res:
        persons_file = os.path.join('files', 'objects.json')

        with open(persons_file,'a') as _file:
            _file.write(request.data)
        if v_version == 2:
            print("Request Saved!")

    return ('valid', 200) if res else ('invalid', 400)

if __name__ == '__main__':
    app.run()



