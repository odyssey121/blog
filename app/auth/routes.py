from flask import redirect, request, render_template, url_for, flash
from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegisterForm
from flask_login import current_user, login_user, logout_user
from app.models import User


@bp.route('/login', methods = ['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email = form.email.data).first()
		if user is None or not user.check_password_hash(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('auth.login'))
		login_user(user, remember = form.remember_me.data)
		return redirect(url_for('index'))
	return render_template('auth/login.html', form = form, title = 'Login')

@bp.route('/register', methods = ['POST', 'GET'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegisterForm()
	if form.validate_on_submit():
		new_user = User(username = form.username.data, email = form.email.data)
		new_user.set_password(form.password.data)
		db.session.add(new_user)
		db.session.commit()
		flash('Congratulations, you are now a registered user!')
		return redirect(url_for('auth.login'))
	return render_template('auth/register.html', form = form, title = 'Register')

@bp.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))


	