# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from flask.ext.wtf import Form
from wtforms.ext.sqlalchemy.orm import model_form
from sqlite3 import IntegrityError

import config


app = Flask(__name__, template_folder='templates')
app.config.from_object(config)

db = SQLAlchemy(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    from models import User, Post

    post_form_class = model_form(Post, base_class=Form, db_session=db.session)

    if request.method == 'POST':

        form = post_form_class(request.form)
        if form.validate():

            post = Post(**form.data)
            post.is_visible = True

            print("{} is creating a new {}'th post!".format(
               post.user.username, len(post.user.posts.all()) + 1))

            db.session.add(post)
            db.session.commit()
            flash('Post created!')

        else:
            flash('Form is not valid! Post was not created.')

    else:
        form = post_form_class()

    posts = Post.query.filter_by(is_visible=True).all()
    return render_template('home.html', form=form, posts=posts)


@app.route('/<post_id>/delete', methods=['POST'])
def delete(post_id):
    from models import User, Post

    post_form_class = model_form(Post, base_class=Form, db_session=db.session)
    form = post_form_class()
    post = Post.query.filter_by(id=post_id).first()
    post.is_visible = False
    db.session.commit()
    posts = Post.query.filter_by(is_visible=True).all()
    return render_template('home.html', form=form, posts=posts)


if __name__ == '__main__':
    from models import *
    db.create_all()

    app.run()