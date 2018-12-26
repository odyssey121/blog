from flask import redirect, request, render_template, url_for, flash
from app import db
from app.auth import bp
from .forms import LoginForm, RegisterForm, ResetPasswordRequestForm, ResetPasswordForm
from flask_login import current_user, login_user, logout_user
from app.models import User
from ..email import send_password_reset_email
from app import db
import jwt

@bp.route('/reset_password/<token>', methods = ['GET', 'POST'])
def reset_password(token):
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	user = User.verify_reset_password_token(token)
	if not user:
		return redirect(url_for('index'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		user.set_password(form.password.data)
		db.session.commit()
		flash('Your password has been reset.')
		return redirect(url_for('.login'))
	return render_template('auth/reset_password.html', form = form)

@bp.route('/reset_password_request', methods = ['GET', 'POST'])
def reset_password_request():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = ResetPasswordRequestForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email = form.email.data).first()
		if user:
			send_password_reset_email(user)
		flash('Check your email for the instructions to reset your password')
		return redirect(url_for('.login'))
	return render_template('auth/reset_password_request.html',
	form = form, title = 'Reset Password')

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
		new_user.password(form.password.data)
		db.session.add(new_user)
		db.session.commit()
		flash('Congratulations, you are now a registered user!')
		return redirect(url_for('auth.login'))
	return render_template('auth/register.html', form = form, title = 'Register')

@bp.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))


	