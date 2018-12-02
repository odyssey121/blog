from app.errors import bp
from flask import render_template
from app import db

@bp.app_errorhandler(404)
def not_fount_error(error):
	return render_template('errors/404.html'), 404