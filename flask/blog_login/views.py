# -*- coding: utf-8 -*-
from flask import (
    Blueprint,
    request,
    redirect,
    render_template,
    flash,
    url_for,
)
from flask.ext.login import (
    login_required,
    login_user,
    logout_user,
    current_user,
)

from models import User
from app import db
from forms import RegisterForm, LoginForm, AddPostForm


auth = Blueprint('auth', __name__, url_prefix='/auth')
views = Blueprint('views', __name__, url_prefix='/')


# Views:


@views.route('/', methods=['GET'])
def index():
    from models import Post

    posts = Post.query.filter_by(is_visible=True).all()
    return render_template('view.html', form=None, posts=posts)





# Auth:


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html', form=RegisterForm())

    form = RegisterForm(request.form)
    if form.validate_on_submit():
        user = User()
        form.populate_obj(user)
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash('User successfully registered')
        return redirect(url_for('.login'))
    else:
        flash('Incorrect registration!')
        return render_template('register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', form=LoginForm())

    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = form.user
        login_user(user, remember=True)
        return redirect(url_for('auth.view'))
    else:
        flash('Incorrect attempt!')
        return render_template('login.html', form=form)


@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return 'You are now logged out'


@auth.route('/view', methods=['GET', 'POST'])
@login_required
def view():
    from models import User, Post

    if request.method == 'POST':

        form = AddPostForm(request.form)
        if form.validate():

            post = Post(title=form.data['title'], content=form.data['content'], user=current_user)
            post.is_visible = True

            print("{} is creating a new {}'th post!".format(
               post.user.username, len(post.user.posts.all()) + 1))
            print post.id

            db.session.add(post)
            db.session.commit()
            flash('Post created!')

        else:
            flash('Form is not valid! Post was not created.')

    else:
        form = AddPostForm()

    posts = Post.query.filter_by(is_visible=True).all()
    return render_template('home.html', form=form, posts=posts)


@auth.route('/<post_id>/delete', methods=['GET'])
@login_required
def delete(post_id):
    from models import User, Post

    form = AddPostForm(request.form)
    post = Post.query.filter_by(id=post_id).first()
    print post.id
    post.is_visible = False
    db.session.commit()
    posts = Post.query.filter_by(is_visible=True).all()
    return render_template('home.html', posts=posts, form=form)

