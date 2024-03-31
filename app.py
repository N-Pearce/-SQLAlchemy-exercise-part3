"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'pwab'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

with app.app_context():
    db.create_all()


### Delete any blank users
# with app.app_context():
#     userx = User.query.filter_by(first_name='').all()
#     for user in userx:
#         db.session.delete(user)
#     db.session.commit()

@app.route('/')
def to_users():
    return redirect('/users')

@app.route('/users')
def show_users():
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/show.html', users=users)

@app.route('/add-user')
def show_form():
    return render_template('users/new.html')

@app.route('/add-user', methods=['POST'])
def add_user():
    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url' or None]
    )
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_id_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('users/details.html', user=user)

@app.route('/users/<int:user_id>/edit')
def edit_screen(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('users/edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']
    db.session.add(user)
    db.session.commit()
    return redirect(f'/users')

@app.route('/users/<int:user_id>/delete')
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')