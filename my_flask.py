from app import app, db
from app.models import User, Article, Comment, Category

@app.shell_context_processor
def make_shell_context():
	return {'db':db, 'User': User, 'app': app, 'Article': Article,
	'Comment': Comment, 'Category': Category}
