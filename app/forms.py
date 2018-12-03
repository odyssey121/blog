from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, DateField
from wtforms.validators import DataRequired, ValidationError, Length, URL, Optional
from app.models import User

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
