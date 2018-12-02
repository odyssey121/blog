from flask import redirect, request, render_template, url_for, flash
from app.auth import bp
from app.auth.forms import LoginForm, RegisterForm
from flask_login import current_user, login_user
from app.models import User


@bp.route('/login', methods = ['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username = form.username.data).first()
		if User is None or not User.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('auth.login'))
		login_user(user, remember_me = form.remember_me.data)
		return redirect(url_for('index'))
	return render_template('auth/login.html', form = form)


	