from app import db
from app.talks import bp
from flask import render_template, url_for, redirect, flash
from flask_login import current_user
from app.talks.forms import TalkForm
from app.models import Talk, User
from datetime import datetime




@bp.route('/')
def index():
	talks = Talk.query.order_by(Talk.date.desc()).all()
	return render_template('talks/index.html', talks = talks, title = 'Talks list')





@bp.route('/new_talk', methods = ['GET', 'POST'])
def new_talk():
	form = TalkForm()
	form.date.data = datetime.now()
	if form.validate_on_submit():
		talk = Talk(title = form.title.data,
			description = form.description.data,
			slides = form.slides.data,
			video = form.video.data,
			venue = form.venue.data,
			venue_url = form.venue_url.data,
			date = form.date.data,
			author = current_user)
		db.session.add(talk)
		db.session.commit()
		flash('The talk was added successfully.')
		return redirect(url_for('index'))
	return render_template('talks/new_talk.html', form = form, title = 'Create Talk')
