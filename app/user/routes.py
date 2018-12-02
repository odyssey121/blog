from flask import render_template, url_for, request
from flask_login import login_required, current_user
from app.user.forms import EditProfileForm
from app import db
from app.user import bp
from app.models import User

@login_required
@bp.route('/<username>')
def user(username):
	user = User.query.filter_by(username = username).first_or_404()
	posts = [
	{'author':user, 'body': 'Test post #1'},
	{'author':user, 'body': 'Test post #1'}]
	return render_template('user/user.html', user = user, posts = posts)

@login_required
@bp.route('/edit_profile', methods = ['POST', 'GET'])
def edit_profile():
	form = EditProfileForm(current_user.username)
	if form.validate_on_submit():
		current_user.username = form.username.data
		current_user.about_me = current_user.about_me
		db.session.commit()
		flash('Your changes have been saved.')
		return redirect(url_for('user.edit_profile'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.about_me.data = current_user.about_me
	return render_template('user/edit_profile.html', form = form , title = 'Edit profile')

