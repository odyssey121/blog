from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, DateField, BooleanField
from wtforms.validators import DataRequired, ValidationError, Length, URL, Optional,Email
from app.models import User
from flask_pagedown.fields import PageDownField


class PresenterCommentForm(FlaskForm):
	body = PageDownField('Comment', validators = [DataRequired()])
	submit = SubmitField('Submit')

class CommentForm(FlaskForm):
	name = StringField('Name', validators = [DataRequired(), Length(min = 3, max =64)])
	email = StringField('Email', validators = [DataRequired(), Length(1,64), Email()])
	body = PageDownField('Comment', validators = [DataRequired()])
	notify = BooleanField('Notify when new comments are posted', default = True)
	submit = SubmitField('Submit')

class EditProfileForm(FlaskForm):
	username = StringField('Username', validators = [DataRequired()])
	about_me = TextAreaField('About me', validators = [Length(min = 0, max = 140)])
	submit = SubmitField('Submit')

	def __init__ (self, original_username, *args, **kwargs):
		super(EditProfileForm, self).__init__(*args, **kwargs)
		self.original_username = original_username

	def validate_username(self, username):
		if username.data != self.original_username:
			user = User.query.filter_by(username = username.data).first()
			if user is not None:
				raise ValidationError('Please use a different username.')

class TalkFor(FlaskForm):
	title = StringField('Title', validators = [DataRequired(), Length(min = 3, max = 140)])
	description = TextAreaField('Description')
	slides = StringField('Slides Embed code (450 pixels wide)')
	video = StringField('Video Embed code (450 pixels wide)')
	venue = StringField('Venue', validators = [DataRequired(), Length(min= 1, max = 128)])
	venue_url = StringField('Venue URL', validators= [Length(min = 1, max = 128), URL()])
	date = DateField('Date')
	submit = SubmitField('Submit')
