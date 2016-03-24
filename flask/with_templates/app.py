# -*- coding: utf-8 -*-

from flask import Flask, request, render_template

import config
from forms import ContactForm
from models import Storage, BlogPostModel, PostDecoder, PostEncoder
import datetime
import json
import os
import qrcode
import base64
import StringIO


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')

    func()

app = Flask(__name__, template_folder='templates')
app.config.from_object(config)


@app.route('/', methods=['GET', 'POST'])
def home():

    storage = Storage()
    items_to_validate = storage.items

    if request.method == 'POST':
        form = ContactForm(request.form)
        if form.validate():
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=5,
                border=4,
            )
            qr.add_data(form.data['title'])
            qr.make(fit=True)
            img = qr.make_image()

            buff = StringIO.StringIO()
            img.save(buff, 'GIF')
            encoded_data = base64.b64encode(buff.getvalue())
            model = BlogPostModel(datetime.datetime.now(),form.data['title'],form.data['text'],encoded_data)
            items_to_validate.append(model)
    else:
        form = ContactForm()

    return render_template('home.html',
                           form=form,
                           items=items_to_validate,
                           )

@app.route('/shutdown', methods=['GET'])
def shutdown():
    shutdown_server()
    storage=Storage()
    with open(persons_file, 'w') as _file:
        result_json = PostEncoder().encode(storage.items)
        _file.write(result_json)

    return 'Server shutting down...'


if __name__ == '__main__':
    storage = Storage()

    persons_file = os.path.join('files', 'objects.json')

    with open(persons_file) as _file:
        models = json.load(_file, cls=PostDecoder)
        storage.items = models

    app.run()



