from app import db
from app.articles import bp
from flask import render_template, url_for, redirect, flash, request
from flask_login import current_user
from app.articles.forms import ArticleForm
from app.models import Article, User
from datetime import datetime

@bp.route('/')
@bp.route('/index')
def index():
	articles_list = Article.query.order_by(Article.date.desc()).all()
	return render_template('articles/index.html', articles_list = articles_list,
	title = 'Articles')


@bp.route('/edit/<int:id>', methods = ['POST', 'GET'])
def edit(id):
	article = Article.query.get_or_404(id)
	if current_user != article.author:
		abort(403)
	form = ArticleForm(obj = article)
	if form.validate_on_submit():
		form = ArticleForm(formdata = request.form, obj = article)
		form.populate_obj(obj = article)
		db.session.commit()
		flash('The talk was updated successfully.')
		return redirect(url_for('articles.article', id = article.id))
	return render_template('articles/edit_article.html', form = form ,
		title = 'Edit Article')


@bp.route('<username>')
def user(username):
	user = User.query.filter_by(username = username).first_or_404()
	articles_list = user.articles.order_by(Article.date.desc()).all()
	return render_template('articles/index.html', articles_list = articles_list,
	title = 'Articles by {}'.format(user.username))

@bp.route('/<int:id>')
def article(id):
	article = Article.query.get_or_404(id)
	return render_template('articles/article.html', article = article, 
	title = 'Article {}'.format(article.title))


@bp.route('/new_article', methods = ['GET', 'POST'])
def new_article():
	form = ArticleForm()
	form.date.data = datetime.now()
	if form.validate_on_submit():
		article = Article(title = form.title.data,
			description = form.description.data,
			slides = form.slides.data,
			video = form.video.data,
			venue = form.venue.data,
			venue_url = form.venue_url.data,
			date = form.date.data,
			author = current_user)
		db.session.add(article)
		db.session.commit()
		flash('The article was added successfully.')
		return redirect(url_for('articles.index'))
	return render_template('articles/new_article.html', form = form, title = 'Create Article')
