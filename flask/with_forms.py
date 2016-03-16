from flask import Flask, request

# pip install flask-WTF
from flask.ext.wtf import Form
from wtforms import StringField, validators


class ContactForm(Form):
    name = StringField(label='Name', validators=[
        validators.Length(min=4, max=25)
    ])
    email = StringField(label='E-mail', validators=[
        validators.Length(min=6, max=35), validators.Email()
    ])


app = Flask(__name__)
app.config.update(
    DEBUG=True,
    SECRET_KEY='This key must be secret!',
    WTF_CSRF_ENABLED=False,
)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        print(request.form)
        form = ContactForm(request.form)
        return ('valid', 200) if form.validate() else ('invalid', 400)
    return 'hello world!', 200

if __name__ == '__main__':
    app.run()
