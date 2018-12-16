from app import app, db
from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models import User, Comment, Article
from app.forms import EditProfileForm
from datetime import datetime

@app.before_request
def before_request():
	if current_user.is_authenticated:
		current_user.last_seen = datetime.utcnow()
		db.session.commit()

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')


@app.route('/moderate')
@login_required
def moderate():
	articles = Article.query.all()

	comment_list_not_approve = Comment.query.filter(Comment.approved == False)
	comments = comment_list_not_approve.order_by(Comment.timestamp.desc()).all()
	return render_template('moderate/moderate.html', comments = comments, title = 'moderate')




@app.route('/user/<username>')
@login_required
def user(username):
	user = User.query.filter_by(username = username).first_or_404()
	posts = [
	{'author':user, 'body': 'Test post #1'},
	{'author':user, 'body': 'Test post #1'}]
	return render_template('user/user.html', user = user, posts = posts, title = 'Profile')


@app.route('/edit_profile', methods = ['POST', 'GET'])
@login_required
def edit_profile():
	form = EditProfileForm(current_user.username)
	if form.validate_on_submit():
		current_user.username = form.username.data
		current_user.about_me = form.about_me.data
		db.session.commit()
		flash('Your changes have been saved.')
		return redirect(url_for('edit_profile'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.about_me.data = current_user.about_me
	return render_template('user/edit_profile.html', form = form , title = 'Edit profile')

