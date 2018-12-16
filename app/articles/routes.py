from app import db
from app.articles import bp
from flask import render_template, url_for, redirect, flash, request,abort
from flask_login import current_user, login_required
from app.articles.forms import ArticleForm
from app.forms import PresenterCommentForm, CommentForm
from app.models import Article, User, Comment
from datetime import datetime

@bp.route('/')
@bp.route('/index')
def index():
	articles_list = Article.query.order_by(Article.date.desc()).all()
	return render_template('articles/index.html', articles_list = articles_list,
	title = 'Articles')

@bp.route('/edit/<int:id>', methods = ['POST', 'GET'])
@login_required
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

@bp.route('/<int:id>', methods = ['GET', 'POST'])
def article(id):
	article = Article.query.get_or_404(id)
	comment = None
	if current_user.is_authenticated:
		form = PresenterCommentForm()
		if form.validate_on_submit():
			comment = Comment(body = form.body.data, article = article,
				author = current_user, notify = False, approved = True)
	else:
		form = CommentForm()
		if form.validate_on_submit():
			comment = Comment(body = form.body.data, article = article,
				author_name = form.name.data, author_email = form.email.data,
				notify = form.notify.data, approved = False)
	if comment:
		db.session.add(comment)
		db.session.commit()
		if comment.approved:
			flash('Your comment has been published.')
		else:
			flash('Your comment will be published after it is reviewed by the presenter.')
		return redirect(url_for('.article', id = article.id) + '#top')
	comments = article.comments.order_by(Comment.timestamp.asc()).all()
	return render_template('articles/article.html', article = article, 
	title = 'Article {}'.format(article.title), form = form , comments = comments)

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

@bp.route('/moderate')
@login_required
def moderate():
	comments = current_user.for_moderation().order_by(Comment.timestamp.asc())
	return render_template('articles/moderate.html', comments = comments)

@bp.route('/moderate-admin')
@login_required
def moderate_admin():
	comments = Comment.for_moderation().order_by(Comment.timestamp.asc())
	return render_template('articles/moderate.html', comments = comments)


