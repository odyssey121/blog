from app import db
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from app import login 
from hashlib import md5

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(64), index = True, unique = True)
	email = db.Column(db.String(120), index = True, unique = True)
	password_hash = db.Column(db.String(128))
	about_me = db.Column(db.String(180))
	last_seen = db.Column(db.DateTime, default = datetime.utcnow)

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password_hash(self, password):
		return check_password_hash(self.password_hash, password)

	def __repr__(self):
		return '<User {} id {} >'.format(self.username, self.id)