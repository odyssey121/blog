from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, DateField
from wtforms.validators import DataRequired, Length, URL, Optional


class TalkForm(FlaskForm):
	title = StringField('Title', validators = [DataRequired(), Length(min = 3, max = 140)])
	description = TextAreaField('Description')
	slides = StringField('Slides Embed code (450 pixels wide)')
	video = StringField('Video Embed code (450 pixels wide)')
	venue = StringField('Venue', validators = [DataRequired(), Length(min= 1, max = 128)])
	venue_url = StringField('Venue URL', validators= [Optional(), Length(min = 1, max = 128), URL()])
	date = DateField('Date')
	submit = SubmitField('Submit')
