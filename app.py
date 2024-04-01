"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

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

with app.app_context():
    postx = Post.query.filter_by(user_id=None).all()
    for post in postx:
        db.session.delete(post)
    db.session.commit()

@app.route('/')
def to_users():
    return redirect('/users')

### Start of Users

@app.route('/users')
def show_all_users():
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/show.html', users=users)

@app.route('/add-user')
def show_new_user_form():
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
def show_user(user_id):
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter(Post.user_id == user.id)
    return render_template('users/details.html', user=user, posts=posts)

@app.route('/users/<int:user_id>/edit')
def edit_user_screen(user_id):
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

    # removes user and all their posts
    # couldn't figure out how to cascade
    db.session.delete(user)
    deleted_posts = Post.query.filter_by(user_id=None).all()
    for post in deleted_posts:
        db.session.delete(post)

    db.session.commit()
    return redirect('/users')

### Start of Posts

@app.route('/posts')
def show_all_posts():
    posts = Post.query.order_by(Post.title).all()
    return render_template('posts/show.html', posts=posts)

@app.route('/users/<int:user_id>/posts/new')
def show_new_post_form(user_id):
    tags = Tag.query.all()
    return render_template('/posts/new.html', user_id=user_id, tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def add_user_post(user_id):
    new_post = Post(
        title=request.form['title'],
        content=request.form['content'],
        user_id=user_id
    )

    tag_ids = [int(num) for num in request.form.getlist('tags')]
    new_post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(new_post)
    db.session.commit()
    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(post.user_id)
    return render_template('posts/details.html', post=post, user=user)

@app.route('/posts/<int:post_id>/edit')
def edit_post_screen(post_id):
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template('/posts/edit.html', post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    tag_ids = [int(num) for num in request.form.getlist('tags')]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    
    db.session.add(post)
    db.session.commit()
    return redirect(f'/posts/{post_id}')

@app.route('/posts/<int:post_id>/delete/<int:user_id>')
def delete_post(post_id, user_id):
    post = Post.query.get_or_404(post_id)

    deleted_post_tags = PostTag.query.filter_by(post_id=post.id).all()
    for post_tag in deleted_post_tags:
        db.session.delete(post_tag)

    db.session.delete(post)
    db.session.commit()
    return redirect(f'/users/{user_id}')

### Start of Tags

@app.route('/tags')
def show_all_tags():
    tags = Tag.query.order_by(Tag.name).all()
    return render_template('tags/show.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def show_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tags/details.html', tag=tag)

@app.route('/tags/new')
def show_new_tag_form():
    return render_template('tags/new.html')

@app.route('/tags/new', methods=['POST'])
def add_tag():
    new_tag = Tag(
        name=request.form['name']
    )
    db.session.add(new_tag)
    db.session.commit()
    return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit')
def edit_tag_screen(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template('/tags/edit.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def edit_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    db.session.add(tag)
    db.session.commit()
    return redirect(f'/tags/{tag_id}')

@app.route('/tags/<int:tag_id>/delete')
def delete_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    deleted_post_tags = PostTag.query.filter_by(tag_id=tag.id).all()
    for post_tag in deleted_post_tags:
        db.session.delete(post_tag)

    db.session.delete(tag)
    db.session.commit()
    return redirect(f'/tags')