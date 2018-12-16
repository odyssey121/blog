from app import db
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from app import login # and for @user_loader decorations
from hashlib import md5
#Because Flask-Login knows nothing about databases,
#it needs the application's help in loading a user.
#For that reason, the extension expects that the application will
#configure a user loader function, 
#that can be called to load a user given the ID.
from markdown import markdown
import bleach
import re

@login.user_loader
def load_user(id):
	return User.query.get(int(id))

class Comment(db.Model):
	__tablename__ = 'comments'
	id = db.Column(db.Integer, primary_key = True)
	body = db.Column(db.Text)
	body_html = db.Column(db.Text)
	timestamp = db.Column(db.DateTime, index = True, default = datetime.utcnow)
	author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	author_name = db.Column(db.String(64))
	author_email = db.Column(db.String(64))
	notify = db.Column(db.Boolean, default = True)
	approved = db.Column(db.Boolean, default = False)
	article_id = db.Column(db.Integer, db.ForeignKey('articles.id'))
	@staticmethod
	def on_changed_body(target, value, oldvalue, initiator):
		allowed_tags = ['a','abbr','acronym', 'b','blockquote','code',
		'em','i','li','ol','pre','strong','ul','h1','h2','h3','p']
		target.body_html = bleach.linkify(bleach.clean(markdown(value,output_format='html'),
			tags = allowed_tags, strip = True))


articles_categories = db.Table('articles_categories',
	db.Column('article_id', db.Integer, db.ForeignKey('articles.id')),
	db.Column('category_id', db.Integer, db.ForeignKey('categories.id')))


class Article(db.Model):
	__tablename__ = 'articles'
	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String(128), nullable = False)
	description = db.Column(db.Text)
	slides = db.Column(db.Text())
	video = db.Column(db.Text())
	venue = db.Column(db.String(128))
	venue_url = db.Column(db.String(128))
	date = db.Column(db.DateTime())
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	comments = db.relationship('Comment', lazy = 'dynamic', backref = 'article')
	categories = db.relationship('Category', secondary = articles_categories,
		backref = db.backref('articles', lazy = 'dynamic'))

def slugify(r):
	pattern = r'[^\w]'
	return re.sub(pattern, '-', r)


class Category(db.Model):
	__tablename__ = 'categories'
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(30), unique = True)
	slug = db.Column(db.String(30))
	@staticmethod
	def generate_slug(target, value, oldvalue, initiator):
		target.slug = slugify(value)

	def add(self, article):
		self.articles.append(article)

	def __repr__(self):
		return '<Cetegory {} id {}>'.format(self.name, self.id)
<<<<<<< HEAD
=======



>>>>>>> 20cb8e5d877baba3bfd3e6642aaff23ddb482ab6

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(64), index = True, unique = True)
	email = db.Column(db.String(120), index = True, unique = True)
	password_hash = db.Column(db.String(128))
	about_me = db.Column(db.String(180))
	last_seen = db.Column(db.DateTime, default = datetime.utcnow)
	articles = db.relationship('Article', backref = 'author', lazy = 'dynamic')
	comments = db.relationship('Comment', backref = 'author', lazy = 'dynamic')


	def avatar(self, size):
		digest = md5(str(self.email).lower().encode('utf-8')).hexdigest()
		return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
			digest, size)

	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password_hash(self, password):
		return check_password_hash(self.password_hash, password)

	def __repr__(self):
		return '<User {} id {} >'.format(self.username, self.id)


db.event.listen(Comment.body, 'set', Comment.on_changed_body)
db.event.listen(Category.name, 'set', Category.generate_slug)
